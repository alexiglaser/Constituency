# Get the hex coordinates of every polyhex
all_hex_coords = function(size = 2, q_shape = 'even', hex_x = 0, hex_y = 0, hex_coords = "(0,0)"){
  if (size == 2){
    if ((q_shape == 'even' & (hex_x %% 2 == 0)) | (q_shape == 'odd' & (hex_x %% 2 == 1))){
      coords = data.frame(
        shape = 'shape1',
        hex_x1 = c(hex_x, hex_x+1, hex_x+1, hex_x, hex_x-1, hex_x-1),
        hex_y1 = c(hex_y+1, hex_y, hex_y-1, hex_y-1, hex_y-1, hex_y)
      )
    } else {
      coords = data.frame(
        shape = 'shape1',
        hex_x1 = c(hex_x, hex_x+1, hex_x+1, hex_x, hex_x-1, hex_x-1),
        hex_y1 = c(hex_y+1, hex_y+1, hex_y, hex_y-1, hex_y, hex_y+1)
      )
    }
    coords = coords %>% mutate(hex_coords = hex_coords, filler1 = paste0("(", hex_x1, ",", hex_y1, ")"))
  }
  if (size == 3){
    # The shape number refers to the order in which they appear on the wikipedia page
    # https://en.wikipedia.org/wiki/Polyhex_(mathematics)
    
    ################################################################
    # Need to fill up shape2 and shape3
    ################################################################
    
    if ((q_shape == 'even' & (hex_x %% 2 == 0)) | (q_shape == 'odd' & (hex_x %% 2 == 1))){
      coords = data.frame(
        shape = rep('shape1', 6), rep('shape2', 6), rep('shape3', 6),
        hex_x1 = c(hex_x, hex_x+1, hex_x+1, hex_x, hex_x-1, hex_x-1),
        hex_y1 = c(hex_y+1, hex_y, hex_y-1, hex_y-1, hex_y-1, hex_y),
        hex_x2 = c(hex_x, hex_x+2, hex_x+2, hex_x, hex_x-2, hex_x-2),
        hex_y2 = c(hex_y+2, hex_y+1, hex_y-1, hex_y-2, hex_y-1, hex_y+1)
      )
    } else {
      coords = data.frame(
        shape = rep('shape1', 6), rep('shape2', 6), rep('shape3', 6),
        hex_x1 = c(hex_x, hex_x+1, hex_x+1, hex_x, hex_x-1, hex_x-1),
        hex_y1 = c(hex_y+1, hex_y+1, hex_y, hex_y-1, hex_y, hex_y+1),
        hex_x2 = c(hex_x, hex_x+2, hex_x+2, hex_x, hex_x-2, hex_x-2),
        hex_y2 = c(hex_y+2, hex_y+1, hex_y-1, hex_y-2, hex_y-1, hex_y+1)
      )
    }
    coords = coords %>% mutate(
      hex_coords = hex_coords, 
      filler1 = paste0("(", hex_x1, ",", hex_y1, ")"),
      filler2 = paste0("(", hex_x2, ",", hex_y2, ")")
    )
  }
}

