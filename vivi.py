import re
import plotly
import plotly.graph_objs as go

from plotly import tools


def getWARD_SECTION(line):
    result = re.split(r',', line, maxsplit=1)
    WARD_SECTION = re.findall(r'\d{1,5}', result[0])
    if WARD_SECTION:
        return WARD_SECTION[0], result[1]
    else:
        return None, result[1]

def getWARD(line):
    result = re.split(r',', line, maxsplit=1)
    WARD = re.findall(r'\d+', result[0])[0]
    return WARD, result[1]

def getSECTION(line):
    result = re.split(r',', line, maxsplit=1)
    SECTION = re.findall(r'\d+', result[0])[0]
    return SECTION, result[1]

def getMONTH_NAME(line):
    result = re.split(r',', line, maxsplit=1)
    MONTH_NAME = re.findall(r'\w+', result[0])[0]
    return MONTH_NAME, result[1]

def getMONTH(line):
    result = re.split(r',', line, maxsplit=1)
    MONTH = re.findall(r'\d+', result[0])[0]
    return MONTH, result[1]


try:

    with open("C:/cliar/street-sweeping-schedule-2012.csv") as file:
        header = file.readline().rstrip()
        header_nice = [column.strip().upper() for column in header.split(",")]

        dataset = {}

        line_number = 1
        for line in file:
            line = line.strip().rstrip()
            line_number += 1

            if not line:
                continue

            WARD_SECTION, line = getWARD_SECTION(line)
            WARD, line = getWARD(line)
            SECTION, line = getSECTION(line)
            MONTH_NAME, line = getMONTH_NAME(line)
            MONTH, line = getMONTH(line)


            if MONTH_NAME not in dataset:
                dataset[MONTH_NAME] = {}
                                
            if WARD_SECTION not in dataset[MONTH_NAME]:
                dataset[MONTH_NAME][WARD_SECTION]={"WARD":WARD,"SECTION":SECTION}

except IOError as io_error:
    print()


def clearPerMonth():
    dataset_go = dict()

    for key in dataset.keys():
        dataset_go[key] = len(dataset[key].keys())

    return dataset_go


result = clearPerMonth()

bar = go.Bar(
    x=list(result.keys()),
    y=list(result.values()),
    name="Bar"
)

scatter = go.Scatter(
    x=list(result.keys()),
    y=list(result.values()),
    name="Scatter"
)

figure = tools.make_subplots(rows=1, cols=2)

figure.append_trace(bar, 1, 1)
figure.append_trace(scatter, 1, 2)
plotly.offline.plot(figure, filename='project.html')


pie = [go.Pie(
    labels=list(result.keys()),
    values=list(result.values())
)]
plotly.offline.plot(pie, filename='kate.html')
#круговая диаграмма pie не запихивается в project.html, и я не смогла это обойти
#из-зи этого создается отдельный kate.htmlё 