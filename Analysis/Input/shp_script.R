setwd("Input/")
library(tidyverse)
library(sf)
constituency_data = st_read("../Data/gb_wpc_2010_05.shp")
ggplot() +
  geom_sf(data=constituency_data[1]) +
  coord_sf()
