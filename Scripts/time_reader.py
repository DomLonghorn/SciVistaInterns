def time_reader(
    filename="/Testing/jorek_times.txt",
    noofpoints=150,
    start=4000,
    Range=607,
    Testing=False,
):
    """Function which will read a file and return equidistant readings from values within the file.

    The main purpose of this script is to extract temporal data when equidistant time steps weren't
    initally recorded or were recorded in a nonlinear fashion. This script will take in an input file
    and a number of points to record and will return a text file with the specified number of points
    split equitemporally. This is useful when trying to create gifs from some simulated JOREK data.

    Licensed under MPL-2.0

    Args:
        filename (str, optional): _description_. Defaults to "/jorek_times.txt".
        noofpoints (int, optional): _description_. Defaults to 150.
        start (int, optional): _description_. Defaults to 4000.
        Range (int, optional): _description_. Defaults to 607.
    """
    import time
    import os

    # Get directory of this file and then changes the
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if Testing == True:
        dir_list = dir_path.split("\\")
        if len(dir_list) < 2:
            dir_list = dir_path.split("\\")
        dir_list.remove("Scripts")
        dir_list.append("Testing")
        new_dir_path = "\\".join(dir_list)

        file = new_dir_path + filename

        output = new_dir_path + "\TestText.txt"
    else:
        # File to read
        file = dir_path + filename
        # File to write
        output = dir_path + "\TestText.txt"

    # Open file
    with open(file, "r") as f:
        # Read lines
        FLines = f.readlines()
        # Get length
        FLength = len(FLines)

    # Create empty lists
    listofpoints = []
    listOfTimesteps = []
    listofnumbers = []
    CleanedOutputs = []
    FileID = []

    # Range
    count = 0

    # Iterate through lines
    for x in FLines:
        FullString = x
        StringToCut = FullString[0:14]
        FinalString = FullString.replace(StringToCut, "")
        SigFigString = FinalString[0:8]
        StringToConvert = SigFigString.strip()
        NumString = float(StringToConvert)
        # print(NumString)

        if count >= 553:
            NumString = (
                NumString * 10
            )  # Used to handle the difference in significant figures within the dataset (probably a more general solution)

        CleanedOutputs.append(NumString)
        count += 1

    # Get start value
    startval = CleanedOutputs[1]

    # Get end index
    endindex = Range

    # Get end value
    endval = CleanedOutputs[endindex]

    # Initial time step
    initialtimestep = (endval - startval) / noofpoints

    # Iterate through points
    for i in range(noofpoints):
        DummyTimestep = initialtimestep * i
        listOfTimesteps.append(DummyTimestep)
        listofnumbers.append(startval + listOfTimesteps[i])

    for i in range(len(listOfTimesteps)):
        # Find the value that's closest in the file to the given timestep and give its val
        closestval = min(
            enumerate(CleanedOutputs), key=lambda x: abs(x[1] - (listofnumbers[i]))
        )
        FileID.append(start + (10 * closestval[0]))

    # Write file
    with open(output, "w") as fp:
        for item in FileID:
            # write each item on a new line
            fp.write("%s\n" % item)

    fp.close()
