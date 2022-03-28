from fluidoccigen import cluster

nh = 896

out_dir = "$SCRATCHDIR/2022bench"

aspect_ratios = [2, 4, 8]

nb_cores_per_node = cluster.nb_cores_per_node
nbs_nodes = (1, 2, 4, 8)

for aspect_ratio in aspect_ratios:
    nz = nh // aspect_ratio

    for nb_nodes in nbs_nodes:
        nb_mpi_processes = nb_cores_per_node * nb_nodes

        cluster.submit_command(
            f"fluidfft-bench {nz} {nh} {nh} -o {out_dir}",
            name_run=f"fluidfft-bench_{nz}x{nh}x{nh}_np{nb_mpi_processes}",
            nb_nodes=nb_nodes,
            nb_cores_per_node=nb_cores_per_node,
            nb_mpi_processes=nb_mpi_processes,
            omp_num_threads=1,
            ask=False,
            walltime="23:59:58",
        )
