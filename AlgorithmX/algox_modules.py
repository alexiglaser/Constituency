# Modules used in the calculation of AlgorithmX solutions
import numpy as np
import pandas as pd
from AlgorithmX import *
from random import sample
from interruptingcow import timeout
import sys
import logging
TIMEOUT = 120
import gc

def const_mapper(df, log=None):
    """
    As the AlgorithmX code requires inputs starting from zero we shall take all values in the dataframes
    and map them to ints. This function will return the solver required.
    The df is always randomly resampled when we run this so that we get a different initial answer each time.
    """
    df = df.sample(len(df))
    name_cols = get_name_cols(df)
    const_list = np.unique(df[name_cols].stack())
    n = len(const_list)
    mapping = {}
    for i in range(n):
        mapping[const_list[i]] = i
    for col in name_cols:
        df = df.replace({col: mapping})
    solver = AlgorithmX(n)
    gc.collect()
    for index, row in df.iterrows():
        try:
            with timeout(TIMEOUT, exception=RuntimeError): 
                solver.appendRow([r for r in row[name_cols]], row['set_no'])
        except RuntimeError:
            log.warning("Failed to create solver")
            solver = None
            break
    return solver

def return_solutions(df, max_soln = 1e7, resampled=False, log=None):
    """
    This function returns the solutions from the AlgorithmX code.
    prop - states what proportion of the solutions are returned (useful for when they get too big)
    max_soln - maximum number of solutions to derive
    resampled - is this solution being rerun
    """
    # The maximum number of solutions returned by the Algorithm X solver. If more solutions are available we shall
    # rerun but with a resampled dataframe, which, as the results are non-deterministic, should give us a 
    # different set of results.
    max_returned = 2e6
    
    solver = const_mapper(df, log=log)
    if solver is not None:
        solns = 0
        dict_solns = {}
        try:
            with timeout(TIMEOUT, exception=RuntimeError): 
                # Stop calculations if taking too long, either there is no solution or having difficulty finding first one\
                for solution in solver.solve():
                    dict_solns[solns] = solution
                    if solution is None:
                        solns = 0
                        break
                    else:
                        solns += 1
                        if solns == max_soln:
                            resampled = True # As we will be rerunning this with a 'resampled' data frame
                            break
                soln_returned = solns > 0

                # If the result is too big take a sample. If the solution is going to be resampled take a small proportion
                # otherwise take a larger one
                if soln_returned:
                    if not resampled and solns <= max_returned:
                        sampled_solns = pd.DataFrame({'soln': dict_solns}).reset_index(drop=True)
                    else:
                        if not resampled:
                            keys = sample(list(dict_solns.keys()), max_returned)
                        else:
                            keys = sample(list(dict_solns.keys()), int(max_soln*0.0025))
                        dict_solns2 = {}
                        for k in keys:
                            dict_solns2[k] = dict_solns[k]
                        sampled_solns = pd.DataFrame({'soln': dict_solns2}).reset_index(drop=True)
                    # Sort out the solutions at this point to save time later.
                    sampled_solns = sampled_solns.assign(soln = [list(np.sort(s)) for s in sampled_solns['soln']])
                    return soln_returned, sampled_solns, resampled
                else:
                    return soln_returned, None, None
        except RuntimeError:
            log.warning("AlgorithmX took too long")
            soln_returned = False
            return soln_returned, None, None
    else:
        soln_returned = False
        return soln_returned, None, None

def to_remove_names(df):
    """
    from the randomly selected 'set_no' put the names that will be removed into a list
    """
    return df.loc[:, df.columns.str.startswith('name')].values.tolist()[0]

def get_n(df, name_cols):
    """
    Find how many different constituencies there are in a data frame.
    """
    const_list = np.unique(df[name_cols].stack())
    return len(const_list)

def remove_consts(df, to_remove, name_cols):
    """
    Given a list of constituencies (to_remove) remove all rows from dataframe which contain them
    """
    for name in name_cols:
        df = df[~df[name].isin(to_remove)]
    return df

def get_name_cols(df):
    """
    Return all columns that start with the word 'name'
    """
    return df.columns[df.columns.str.startswith('name')]

def remove_random_const(const_pairs, const_tris, const_quads, seats, region, n, log):
    """
    This function removes randomly selected pairs / triplets / quadruplets to make sure
    that the number of constituencies left are divisble by the number of seats.
    """
    n2 = n # Check that the number of remaining constituencies are divisible by n
    if seats == 2:
        name_cols = get_name_cols(const_pairs)
    elif seats == 3:
        name_cols = get_name_cols(const_tris)
    elif seats == 4:
        name_cols = get_name_cols(const_quads)
    removed = {}
    # How many constituencies are removed to make the number remaining divisbile by 'seats'?
    if seats == 2:
        n3 = n2 - 3
    elif (seats == 3) & (n % seats == 1):
        n3 = n2 - 4
    elif (seats == 3) & (n % seats == 2):
        n3 = n2 - 2
    elif seats == 4:
        if n % seats == 1:
            n3 = n2 - 9 # Three triplets are removed
        elif n % seats == 2:
            n3 = n2 - 6 # Two triplets are removed
        elif n % seats == 3:
            n3 = n2 - 3
    if seats == 2:
        while n3 != n2:
            df = const_pairs.copy()
            random_const = const_tris.sample(1)
            log.info(f"Removed {random_const['set_no']} from const_tris")
            removed['triplet'] = random_const['set_no'].iloc[0]
            to_remove = to_remove_names(random_const)
            df = remove_consts(df, to_remove, name_cols)
            n2 = get_n(df, name_cols)
    elif seats == 3:
        while n3 != n2:
            df = const_tris.copy()
            if (seats == 3) & (n % seats == 1):
                random_const = const_quads.sample(1)
                log.info(f"Removed {random_const['set_no']} from const_quads")
                removed['quad'] = random_const['set_no'].iloc[0]
                to_remove = to_remove_names(random_const)
            elif (seats == 3) & (n % seats == 2):
                random_const = const_pairs.sample(1)
                log.info(f"Removed {random_const['set_no']} from const_pairs")
                removed['pair'] = random_const['set_no'].iloc[0]
                to_remove = to_remove_names(random_const)
            df = remove_consts(df, to_remove, name_cols)
            n2 = get_n(df, name_cols)
    elif seats == 4:
        while n3 != n2:
            df = const_quads.copy()
            # Need to ensure that when we remove multiple triplets that none of the elements are repeated
            if (n % seats == 2) or (n % seats == 1):
                df2 = const_tris.copy()
                name_cols2 = df2.columns[df2.columns.str.startswith('name')]
                if n % seats == 1:
                    # remove 3 triplets
                    trips = 3
                elif n % seats == 2:
                    # remove 2 triplets
                    trips = 2
                to_remove = []
                for i in range(trips):
                    random_const = df2.sample(1)
                    if i == 0:
                        removed['triplet'] = [random_const['set_no'].iloc[0]]
                    else:
                        removed['triplet'] = [*removed['triplet'], random_const['set_no'].iloc[0]]
                    to_remove = to_remove + to_remove_names(random_const)
                    # Make sure we only remove applicable sets 
                    for name in name_cols2:
                        df2 = df2[~df2[name].isin(to_remove)]
                removed['triplet'] = list(np.sort(removed['triplet']))
            elif n % seats == 3:
                random_const = const_tris.sample(1)
                removed['triplet'] = random_const['set_no'].iloc[0]
                to_remove = to_remove_names(random_const)
            log.info(f"Removed {removed['triplet']} from const_quads")
            df = remove_consts(df, to_remove, name_cols)
            n2 = get_n(df, name_cols)

    return df, removed

def custom_logger(logger_name, level=logging.DEBUG):
    """
    Method to return a custom logger with the given name and level
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    format_string = ('%(levelname)s: %(asctime)s: %(message)s')
    log_format = logging.Formatter(format_string)
    # Creating and adding the console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    # Creating and adding the file handler
    file_handler = logging.FileHandler(logger_name, mode='a')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    return logger

def get_solns(const_pairs, const_tris, const_quads, seats, region, max_solns=1e6):
    """
    Find the solutions, or a subset of them, and saves them into a csv file
    """
    const_pairs2 = const_pairs.query("region == @region")
    const_tris2 = const_tris.query("region == @region")
    const_quads2 = const_quads.query("region == @region")
    if seats == 2:
        df = const_pairs2
    elif seats == 3:
        df = const_tris2
    elif seats == 4:
        df = const_quads2
    name_cols = get_name_cols(df)
    # How many times should we rerun Algorithm X when we cannot return all solutions.
    RERUN_COUNTER = 40 * (1 + (seats >= 4))
    # How many times should we rerun Algorithm X when we have to remove a random constituency set so that the 
    # number of constituencies left are divisible by `seats`.
    COUNTER = 30 * (1 + (seats >= 4))
    LONG_TIMEOUT = 300
    
    n = get_n(df, name_cols)
    r = region.replace(" ", "_")
    file_name = f"Solutions/solns_{r}_{seats}.csv.gz"
    log_file_name = f"Logs/log_{r}_{seats}.log"
    log = custom_logger(log_file_name)
    if n % seats == 0:
        try:
            with timeout(LONG_TIMEOUT, exception=RuntimeError): 
                soln_returned, solns, resampled = return_solutions(df, resampled=False, max_soln=max_solns, log=log)
        except RuntimeError:
                log.warning(f"For the {region} region, when we have {seats} seats there is a timeout.")
                soln_returned = False
        if soln_returned:
            if len(solns) <= 1 or solns is None:
                log.warning(f"For the {region} region, when we have {seats} seats there are no solutions.")
            else:
                # If we're unable to get all solutions rerun multiple times to get a further subset of them.
                if resampled:
                    d = {}
                    d[0] = solns.copy()
                    j = 0
                    while j < RERUN_COUNTER:
                        log.info(f"At j = {j}.") 
                        try:
                            with timeout(LONG_TIMEOUT, exception=RuntimeError): 
                                soln_returned, d[j], resampled = return_solutions(df, resampled=True, max_soln=max_solns, log=log)
                        except RuntimeError:
                                log.warning(f"For the {region} region, when we have {seats} seats there is a timeout.")
                                soln_returned = False
                        if soln_returned:
                            j += 1
                    if soln_returned:
                        try:
                            solns = pd.concat(d, ignore_index=True)
                        except:
                            log.warning(f"For region {region} with seats = {seats} we cannot concatenate.")
        else:
            log.warning(f"Issue with the {region} region, when we have {seats} seats there are no solutions returned.")
    else:
        # Get the solutions multiple times with different random elements removed.
        soln_dict = {}
        i = 0
        while i < COUNTER:
            log.info(f"At i = {i}.")
            df, removed = remove_random_const(const_pairs2, const_tris2, const_quads2, seats, region, n, log)
            try:
                with timeout(LONG_TIMEOUT, exception=RuntimeError): 
                    soln_returned, soln_dict[i], resampled = return_solutions(df, resampled=False, max_soln=max_solns, log=log)
            except RuntimeError:
                log.warning(f"For the {region} region, when we have {seats} seats there is a timeout.")
                soln_returned = False
            if soln_returned:
                if resampled:
                    d = {}
                    d[0] = soln_dict[i].copy()
                    j = 0
                    while j < RERUN_COUNTER: # and soln_returned:
                        log.info(f"At j = {j}.")
                        try:
                            with timeout(LONG_TIMEOUT, exception=RuntimeError): 
                                soln_returned, d[j], resampled = return_solutions(df, resampled=True, max_soln=max_solns, log=log)
                        except RuntimeError:
                                log.warning(f"For the {region} region, when we have {seats} seats there is a timeout.")
                                soln_returned = False
                        if soln_returned:
                            j += 1
                    if soln_returned:
                        try:
                            soln_dict[i] = pd.concat(d, ignore_index=True)
                        except:
                            log.warning(f"For region {region} with seats = {seats} we cannot concatenate.")
            if soln_returned:
                try:
                    # Add in the set_no's that were removed from the solutions
                    soln_dict[i][list(removed.keys())[0]] = str(list(removed.values())[0])
                    i += 1
                except:
                    for k in range(len(soln_dict)):
                        log.warning(f"{k}: {soln_dict[k].shape}")
                    log.warning(f"For region {region} with seats = {seats} we cannot add in the removed solutions.")
        try:
            solns = pd.concat(soln_dict, ignore_index=True)
        except:
            for k in range(len(soln_dict)):
                log.warning(f"{k}: {soln_dict[k].shape}")
            log.warning(f"For region {region} with seats = {seats} we cannot concatenate solutions.")
    try:
        if len(solns) > 0:
            solns = solns.assign(region = region)
            solns.to_csv(file_name, index=False, compression='gzip')
            log.info(f"Finished getting solutions for region {region} with {seats} seats")
    except:
        log.warning(f"Cannot get solutions for region {region} with {seats} seats")
