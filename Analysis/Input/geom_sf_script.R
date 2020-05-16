# From this code we need to convert each hexagon into hexagonal coordinates
library(parlitools)
library(tidyverse)
library(rlang)
library(purrr)
library(sf)
df = as.data.frame(west_hex_map)
regions = df %>% select('region_name') %>% unique
# We'll use the coordinate susyem mentioned here:
# https://www.redblobgames.com/grids/hexagons/
# We'll loop over each region, ordering the x-values, but semi-oredring the y_values, so highest two values
# get the value 0, the next two highest get the value 1, etc, etc.
# It'll be a bit labour
region = "London Euro Region"
df_region = df %>% filter(region_name == region)
# Need to find the min and max of each polygon shape
df_region2 = df_region %>% 
  mutate(geometry = map(geometry, ~ as.data.frame(.x[[1]]))) %>% 
  unnest(geometry) %>% 
  mutate( # Reduce to 6 significant figures as there can some differences at higher decimal places
    V1 = signif(V1),
    V2 = signif(V2)
  )
df_region3 = df_region2 %>% 
  group_by(object_id) %>% 
  summarise(
    min_x = min(V1), max_x = max(V1), min_y = min(V2), max_y = max(V2)
  )
df_region4 = df_region %>% merge(df_region3)

# We're putting 
order_x = df_region4 %>% select(min_x) %>% unique() %>% mutate(hex_x = rank(min_x) - 1)
order_y = df_region4 %>% select(min_y) %>% unique() %>% mutate(hex_y = floor((rank(min_y) - 1)/2))
df_region5 = 
  df_region4 %>% 
  merge(order_x) %>% 
  merge(order_y) %>% 
  mutate(hex_coords = paste0("(", hex_x, ",", hex_y, ")"))

# Now for each polyhex we need to find all of the possible coordinates it can take.
# Start of with a shape of size 2 to keep things simple.
# If we start in coordinates (x, y), then the second element will be in 
# x even: (x, y+1), (x + 1, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y)
# x odd : (x, y+1), (x + 1, y + 1), (x + 1, y), (x, y - 1), (x - 1, y), (x - 1, y + 1)
# Find where the lowest point of y is and the value of x there to decide is we are in an x-odd or x-even plot
overall_min_y = min(df_region5$min_y)
x_values = df_region5 %>% filter(min_y == overall_min_y) %>% select(hex_x) %>% pull
if (all(x_values %%2 == 0)){
  q_shape == 'even'
} else if (all(x_values %%2 == 1)){
  q_shape == 'odd'
} else {
  print("Can't work out if the hexplots are 'odd-q' or 'even-q")
  stop()
}

  

# Need to work out why we have 6 min and max x's when there are only 5 in the plot


sapply(df_region$geometry, function(x) x %@% 'bbox')

df_region %>% group_by('object_id') %>% select(geometry) %>% map(function(x) x %@% 'bbox')

test = df[df$object_id == 641,]$geometry
# finding the maximum and minimum and assigning hexagonal coordinates to each one
# 
# There's a bit of an issue with some of the 'island' constituencies


west_hex_map %>% #filter(region_name == "Northern Ireland") %>% 
  ggplot() + geom_sf(aes(fill=region_name))

london_hex_map = west_hex_map %>% filter(region_name == "London Euro Region")
ggplot(data = london_hex_map) + geom_sf() + geom_sf_text(aes(label=object_id)) #aes(fill=region_name))

scotland_hex_map = west_hex_map %>% filter(region_name == "Scotland Euro Region")
ggplot(data = scotland_hex_map) + geom_sf() + geom_sf_text(aes(label=object_id))

region = "Northern Ireland"
regional_hex_map = west_hex_map %>% filter(region_name == region)
ggplot(data = regional_hex_map) + geom_sf() + geom_sf_text(aes(label=object_id)) + ggtitle(region)
#aes(fill=region_name))

/var/folders/14/42mdq9gj1lz9fk8hjrqy7xxm0000gn/T//RtmpAFJVEz/downloaded_packages

ggplot(data = london_hex_map) + geom_sf() +
  theme(axis.text=element_blank(),
        axis.ticks=element_blank())

west_hex_map %>% filter(region_name == "Northern Ireland") %>% 
  ggplot() + geom_sf() + 
  theme(axis.text=element_blank(),
        axis.ticks=element_blank()) + geom_sf_text(aes(label=object_id))
