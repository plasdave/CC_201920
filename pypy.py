import math  # import constants (pi, e,...) and other things
# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import atexit

# plt.ion()
# constants
M = 2.824
NB_POINTS = 3 / 5
# K =
# w =
good_data = 'Accelerometer Data 2019-11-13 14-39-03.txt'
testing_shit = 'test2.csv'
file_name = good_data


# functions
def import_data(file_name):
    ''' Import data into a list
        input (str): file name
        output (list): just data in list
    '''
    file1 = open(file_name)
    file2 = file1.read().splitlines()
    for res in range(len(file2)):
        file2[res] = file2[res].split(',')
    return file2


def choose_data(file2, x=0, y=2):
    '''

    :param file2: list of data
    :param x: index of x data column (usually time)
    :param y: index of y data column (acceleration)
    :return: a list with only needed data to calculate
    '''
    db_final = []
    for i in range(1, len(file2)):  # convert values from string to float
        db_final.append([float(file2[i][x]), float(file2[i][y])])
    return db_final


def avr(a_list):
    """ Calculate average value from a list of value
        input (list): list of values
        output (float): average value
    """
    result = 0
    for i in a_list:
        result += i
    result = result / len(a_list)
    return result


def make_plot(db_final):  # This function makes the plot that you see
    list_acc = []
    list_time = []
    for i in range(len(db_final)):
        list_acc.append(db_final[i][1])
        list_time.append(db_final[i][0])
    fig = plt.figure()
    ax = fig.add_axes([0.12, 0.09, 0.87, 0.85])
    ax.scatter(list_time, list_acc, s=4)
    ax.set_xlabel('Temps (s)')
    ax.set_ylabel('Acceleration (m/s^2)')
    ax.set_title('Accélération en fonction du temps')
    plt.show()
    return list_time, list_acc


# print(db)8
# print(db_final)

# Make graph

def find_max_pts(db_final):
    '''
    Find local maxima form the function
    :param db_final: list of maximum points
    :return: list of max points
    '''
    max_pts = []
    for i in range(1, len(db_final) - 1):  # find maximum points on the graph
        if db_final[i][1] > db_final[i + 1][1] and db_final[i][1] > db_final[i - 1][1] and db_final[i][1] > 0:
            max_pts.append([db_final[i][0], db_final[i][1]])
    # print('max_pts: ' + str(max_pts))
    return max_pts


'''
T_list = []
max_better = [] # remove noise
for i in range(1,len(max_pts)):
    if 0.17 > max_pts[i][0]-max_pts[i-1][0] > 0.16:
        max_better.append(max_pts[i])
        T_list.append(max_pts[i][0]-max_pts[i-1][0])
'''


def calc_f(max_pts):
    '''
    Calculate average frequency (supposed to be constant) of the oscillation using maxima of function
    input: list of points
    output: frequency of the signal/oscillation
    '''
    #	print(len(max_pts))
    some_list = [[max_pts[1][0] - max_pts[0][0]]]
    for i in range(2, int(len(max_pts) * NB_POINTS)):
        val = max_pts[i][0] - max_pts[i - 1][0]
        temp = False
        j = 0
        while not temp:
            val_avr = avr(some_list[j])
            if j < len(some_list) - 1:
                if 19 / 20 * val_avr < val < 21 / 20 * val_avr:
                    some_list[j].append(val)
                    temp = True
                else:
                    j += 1
            else:
                some_list.append([val])
    #	print(some_list)
    average_T = avr(some_list[0])
    freq = len(some_list[0])
    #	print('T = ', average_T, 'freq = ', freq)
    for i in range(1, len(some_list)):
        if len(some_list[i]) > freq:
            freq = len(some_list[i])
            average_T = avr(some_list[i])
    average_f = 1 / average_T
    return average_f


'''
#print(T_list)
T_avr = avr(T_list) # average value of period
f = 1/T_avr
'''


def calc_A(max_better):
    '''
    :param max_better: list of local maxima
    :return:
    '''
    ## Find the damping coefficient
    t = []  # list of time
    X = []  # list of positions
    t_sq = []  # list of squared values of t
    Xt = []
    # print(max_better)
    for i in range(len(max_better)):
        t.append(max_better[i][0] - max_better[0][0])
        if max_better[i][1] > 0:
            X.append(math.log(max_better[i][1], math.e))  # t turned into ln(t)
        else:
            X.append(X[len(X) - 1])
        t_sq.append(t[i] ** 2)
        Xt.append(X[i] * t[i])

    # print(t, X, t_sq, Xt, sep='\n')
    avr_tsq = avr(t_sq)
    avr_X = avr(X)
    avr_t = avr(t)
    avr_Xt = avr(Xt)

    Var = avr_tsq - avr_t ** 2
    Cov = avr_Xt - avr_X * avr_t

    a = Cov / Var
    # print('a =',a)
    b = avr_X - a * avr_t
    # print('b =',b)
    return a  # -math.log(X[0],math.e)


# print('list t: ', t)
# print('list X: ', X)
# print(T_better)


def calc_b_and_wn(w_d, A, M):  # A = -xi*w_n, w_d = w_n*sqrt(1-xi**2)
    '''
    Find damping coefficient (B) and natural frequency of the structure (w_n) (without damping)
    :param w_d:
    :param A: -xi*w_n found by calc_A
    :param M: mass of the main (vibrating) structure
    :return: natural frequency (w_n), stiffness (K) and damping coefficient (B)
    '''
    xi = math.sqrt((A / w_d) ** 2 / (1 + (A / w_d) ** 2))
    # print('-A/xi = ', -A/xi)
    # print(w_d/math.sqrt(1-xi**2))
    w_n = (-A / xi) / (2*math.pi)
    k = (2 * math.pi * w_n * math.sqrt(M)) ** 2
    b = 2 * xi * math.sqrt(k * M)
    return w_n, k, b, xi


if __name__ == '__main__':
    useful_data = choose_data(import_data(file_name))
    max_pts = find_max_pts(useful_data)
    w_d = calc_f(max_pts)
    A = calc_A(max_pts[0:int(len(max_pts) * NB_POINTS)])
    w_n, k, b, xi = calc_b_and_wn(w_d*2*math.pi, A, M)
    print('w_d =', w_d)
    # print('A =', A)
    print('w_n = ', w_n)
    print('K = ', k)
    print('B = ', b)
    print('xi = ', xi)
    make_plot(useful_data)
    make_plot(max_pts)

    atexit.register(input, 'Press Enter to exit...')
