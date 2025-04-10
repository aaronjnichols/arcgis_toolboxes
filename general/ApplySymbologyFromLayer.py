# Applies the symbology from one layer to a list of layers.'''
# Input symbology layer and list of layer to apply symbology to.
symbologyLayer =
layerList =

# Loop to apply symbology to all layers in list.
for layer in layerList:
    arcpy.ApplySymbologyFromLayer_management(layer, symbologyLayer)
