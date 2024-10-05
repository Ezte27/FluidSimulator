PADDING = '9764798127'

# Label each cell in the grid inside of the screen
def getCellKeys(screen_width, screen_height, smoothing_radius) -> dict:
    
    # Dictionary to store cell coordinates and key
    cellKeys = {}

    # Calculate the number of cells in x and y axis
    cellsX = screen_width // smoothing_radius
    cellsY = screen_height // smoothing_radius

    # Loop over all cells inside the screen
    for row in range(cellsY):
        for col in range(cellsX):
            cellKeys[(col, row)] = col + (cellsX * row)
    
    return cellKeys

# Get the cell in which the sample point is on 
def posToCellCoord(samplePoint, smoothingRad):
    cellX = samplePoint[0] // smoothingRad
    cellY = samplePoint[1] // smoothingRad

    return (cellX, cellY)

# Convert a cell coordinate into a single number.
def hashCell(cellX, cellY) -> int:

    # Change x and y to strings
    x = str(cellX)
    y = str(cellY)

    # If different lengths, add padding to one
    if len(x) != len(y):
        while len(x) != len(y):
            if (len(x) - len(y)) < 0:
                x += 'X'
            else:
                y += 'X'
    
    # Finally, turn the padding and value into an integer for math operations later on

    x = x.replace('X', PADDING)
    y = y.replace('X', PADDING)
    hash_value = x + y

    return int(hash_value)

def getKeyFromHash(hash_value, spatialLookupSize):
    return hash_value % spatialLookupSize

# Convert the hash value back into the cell coordinate
def unHashCell(hash_value:int) -> tuple:
    
    # Convert hash_value from int to str
    hash_value = str(hash_value)

    # Calculate the length of the encoded value to split it in half
    n = len(hash_value)

    # Calculate the length of each coordinate
    n_coord = int(n / 2)

    # Split enconded value in half
    x = hash_value[:n_coord]
    y = hash_value[n_coord:]

    # Remove any padding if necessary and turn into an integer
    cellX = int(x.replace('X', PADDING))
    cellY = int(y.replace('X', PADDING))

    return (cellX, cellY)

# Example Usage

smoothingRad = 10
samplePoint = (100, 100)

cellCoord = posToCellCoord(samplePoint, smoothingRad)

print(f"smoothingRad = {smoothingRad}")
print(f"samplePoint = {samplePoint}")
print(f"cellCoord = {cellCoord}")

hashedCell = hashCell(cellCoord[0], cellCoord[1])
print(f"Hashed Cell = {hashedCell}")

unHashedCell = unHashCell(hashedCell)
print(f"UnHashed Cell = {unHashedCell}")

# Now lets try looking for a 3 x 3 grid with cellOffsets

CELL_OFFSETS = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1)]

centerCell = posToCellCoord(samplePoint, smoothingRad)

for offsetX, offsetY in CELL_OFFSETS:

    hashedCell = hashCell(cellCoord[0] + offsetX, cellCoord[1] + offsetY)
    print(f"\nHashed Cell = {hashedCell}")

    key = getKeyFromHash(hashedCell, 100) # spatialLookupSize is just the number of particles in the simulation
    print(f"Cell key = {key}")

    unHashedCell = unHashCell(hashedCell)
    print(f"UnHashed Cell = {unHashedCell}")



# # Example Usage of function getCellKeys

# screen_width = 1000
# screen_height = 800
# smoothing_rad = 100

# cellKeys = getCellKeys(screen_width, screen_height, smoothing_rad)
# print(cellKeys)