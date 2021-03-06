from collections import defaultdict

import dwavebinarycsp
import networkx as nx
from dwave.embedding import embed_qubo

import dimod
import dwave
import numpy as np
from dwave.system import DWaveSampler
from dwave_networkx import chimera_graph
import minorminer

from qubo_solver import solve_qubo

import qubo_solver
import qubo_matrices_helpers

# DATA
from utils.jobshop_helpers import ones_from_sample

# smallest workflow -> chain_strength = 4000

A, b, C, paths, tasks_number, machines_number = qubo_matrices_helpers.get_18_qubits_data()
P = 10

# SOLUTION
D = np.diag(2 * A.transpose().dot(b))
QUBO = P * (A.transpose().dot(A) + D) + C



qubits_number = len(QUBO[0])
# linear, quadratic = qubo_matrices_helpers.prepare_qubo_dicts(QUBO)
# linear, quadratic = qubo_matrices_helpers.prepare_qubo_dicts_dwave(QUBO)
# Q = dict(linear)
# Q.update(quadratic)

# for q in QUBO:
#     print(q)
#
# qubo_graph = nx.Graph()
# for i in range(qubits_number):
#     qubo_graph.add_node(i, weight=QUBO[i,i])
#
# for i in range(qubits_number):
#     for j in range(i+1,qubits_number):
#          qubo_graph.add_edge(i,j,weight=2 * QUBO[i][j])
# print(nx.adjacency_matrix(qubo_graph))
#
# emb_miner = minorminer.find_embedding(qubo_graph, chimera_graph(16))
# print(emb_miner)
# tQ = dwave.embedding.embed_qubo(Q, embedding, chimera_graph(16), chain_strength=70000)

response = DWaveSampler().sample_qubo(tQ, num_reads=100)

# for s in list(response.data()):
#     ones = ones_from_sample(s.sample)
#     print(ones, "Energy: ", s.energy, "Occurrences: ", s.num_occurrences)

#

# print("UNEMBEDED RESULTS")
# source_bqm = dwavebinarycsp.dimod.BinaryQuadraticModel.from_qubo(Q)  # (linear, quadratic, 0, Vartype.BINARY)
# suma = 0
# for i, val in enumerate(dwave.embedding.unembed_sampleset(response, source_bqm=source_bqm, embedding=embedding)):
#     suma += list(response.data())[i].num_occurrences
#     print([s for s in ones_from_sample(val) if int(s[1:]) < 18], list(response.data())[i].num_occurrences, list(response.data())[i].energy, suma,)







# SOLVE WITH BRUTE FORCE (max 20 qubits)
# result_list = qubo_solver.solve_qubo(Q)
# for el in sorted(result_list, key=lambda tup: tup[1])[:20]:
#     print(el)

# SOLVE WITH GUROBI
# sampling_result = qubo_matrices_helpers.solve_with_gurobi(QUBO)
# for s in list(sampling_result.data()):
#     print(ones_from_sample(s.sample), "Energy: ", s.energy, "Occurrences: ", s.num_occurrences)
