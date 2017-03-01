import os


directory = r'pages/'

def mapHelper(directory):

    # create HashMap <page, in-link[]>
    adjList = {}
    file_list = os.listdir(directory)
    for file in file_list:
        adjList[file] = []

    # for each page P, HashMap <page, in-link[]>
    #     if (P contains other pages' inlink ){
    #           add P into those pages' in-link[]
    #     }

    for file in file_list:
        page = open(directory + file, "r")
        source_code = page.read()
        # soup = BeautifulSoup(source_code, "html.parser")
        for filename in file_list:
            if filename != file:
                suffix = filename[0:len(filename) - 4]
            else: continue
            #print(suffix)
            href = r'href="/wiki/' + suffix + r'"'
            if href in source_code:
                adjList[filename].append(file)
        page.close()
        print(file)

    # output G1
    fx = open('G1.txt', 'w')
    for file_name in file_list:
        fx.write(file_name + " ")
        for vertex in adjList[file_name]:
            fx.write(vertex + " ")
        fx.write('\n')
    fx.close()


mapHelper(directory)