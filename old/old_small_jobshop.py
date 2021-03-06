import dwavebinarycsp
from dwave.system import DWaveSampler, EmbeddingComposite
from dwave_qbsolv import QBSolv
from utils import jobshop_helpers


def eight_one_one(a, b, c, d, e, f, g, h):
    return (a + b + c + d + e + f + g + h) == 1



def ten_one_one(a, b, c, d, e, f, g, h, i, j):
    return a + b + c + d + e + f + g + h + i + j == 1


def all_equal(a, b, c):
    return a == b and b == c


def first_one_rest_zero_three(first, arg1, arg2, arg3):
    if first == 1:
        return arg1 == 0 and arg2 == 0 and arg3 == 0
    else:
        return True


def first_one_rest_zero_six(first, arg1, arg2, arg3, arg4, arg5, arg6):
    if first == 1:
        return arg1 == 0 and arg2 == 0 and arg3 == 0 and arg4 == 0 and arg5 == 0 and arg6 == 0
    else:
        return True

def first_one_second_zero(first, second):
    if first == 1:
        return second == 0
    else:
        return True


# csp = dwavebinarycsp.factories.random_2in4sat(8, 4)  # 8 variables, 4 clauses
#

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
jobs = [[2, 1], [1, 2, 1]]
number_of_machines = 2
time_limit = 4
number_of_operations = sum([len(job) for job in jobs])
row_length = number_of_machines * number_of_operations
number_of_qubits = row_length * time_limit

# adding starts once constraint
starts_once_constraints = []
for operation_number in range(number_of_operations):
    tmp_operation = []
    for machine_number in range(number_of_machines):
        tmp_operation.extend(['x{}'.format(operation_number + number_of_operations * machine_number + row_length * time) for time in range(time_limit)])
    starts_once_constraints.append(tmp_operation)

for constraint_variable in starts_once_constraints:
    # print("Adding {}".format(constraint_variable))
    csp.add_constraint(eight_one_one, constraint_variable)
print("Added start once constraint")

# adding one job on one machine constraint
one_job_one_machine_cubits = jobshop_helpers.get_one_job_one_machine_csp(jobs, row_length, number_of_operations, number_of_qubits, time_limit)
for i, qubit_list in enumerate(one_job_one_machine_cubits):
    small = 4
    big = 8
    if len(qubit_list) == big:
        for qubit in qubit_list:
            csp.add_constraint(first_one_second_zero, ['x{}'.format(i), 'x{}'.format(qubit)])
    if len(qubit_list) == small:
        for qubit in qubit_list:
            csp.add_constraint(first_one_second_zero, ['x{}'.format(i), 'x{}'.format(qubit)])
    if (len(qubit_list) != small and len(qubit_list) != big):
        raise Exception

print("Added one job on one machine constraint")


# adding order constraint
order_constraints = jobshop_helpers.csp_get_order_constraint(jobs, number_of_machines, time_limit, number_of_operations)
for constraint in order_constraints:
    # print("Adding {}".f   ormat(constraint))
    for cons_elem in constraint[1]:
        csp.add_constraint(first_one_second_zero, ['x{}'.format(constraint[0]), 'x{}'.format(cons_elem)])

print("Added order constraint")

bqm = dwavebinarycsp.stitch(csp, max_graph_size=16, min_classical_gap=0.9)

Q, offset = bqm.to_qubo()
# print(bqm.to_qubo())


# for i in range(32):
#     print("\'x{}\': 0,".format(i))

sampler = EmbeddingComposite(DWaveSampler())
# response = DWaveSampler().sample_qubo(Q)
response = QBSolv().sample_qubo(Q, solver=sampler, solver_limit=30)
# response = EmbeddingComposite(DWaveSampler()).sample_qubo(Q, num_reads=200)
# print("Response acquired")
for s in list(response.data()):
    ones_number = 0
#     for i in range(32):
#         if (s.sample['x{}'.format(i)]):
#             ones_number += 1
    if ones_number == 0:
        print(csp.check(s.sample), s.sample, "Energy: ", s.energy, "Occurrences: ", s.num_occurrences)



