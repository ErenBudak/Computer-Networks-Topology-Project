This repository contains a project focused on designing, implementing, and analyzing various Data Center Fabric network topologies on Mininet, simulating the requirements of a three-tier (Web, Application, Data) web application.

Within the scope of this project, Linear, Star, Ring, and modern Spine-Leaf network topologies were created and comprehensively compared in terms of performance (latency, bandwidth), reliability (fault tolerance), and infrastructure costs.
Completed Tasks and Content

The following network topologies were successfully coded and analyzed on Mininet:
1. Linear Topology Analysis

    Setup of the basic topology where server racks are connected sequentially.

    Latency calculations between the Web Tier and Data Tier (Critical Path).

    Identification of network bottlenecks using simultaneous iperf tests.

    Investigation of connectivity loss through switch failure simulations.

2. Star Topology Analysis

    Construction of a topology using a single central switch connecting all servers.

    Simultaneous bandwidth tests to measure the aggregate capacity of the network.

    Analysis of the effects of a central switch failure (Single Point of Failure).

    Development of modifications to increase the topology's resilience against link and switch failures (e.g., Star v2 variation with dual switches).

3. Ring Topology with Redundancy

    Implementation of a 6-switch ring structure containing redundant (chordal) links to provide fault tolerance.

    Analysis of hop counts using traceroute before any failures.

    Simulation of single and multiple (dual) link failure scenarios to verify how the network reroutes and maintains connectivity.

4. Spine-Leaf Topology

    Setup of a modern two-tier network infrastructure consisting of 2 Spine and 3 Leaf switches.

    Integration of a load generator (h_loadgen) to simulate external internet traffic.

    Demonstration of the maximum hop count and predictable, consistent latency times.

    Measurement of the network's survivability and performance changes when a Spine switch is disabled.

5. Comparative Analysis and Automated Stress Testing

    A detailed comparison table of the topologies in terms of infrastructure cost (number of switches/links), latency, and post-failure connectivity.

    stress_test.py Script: A Python script that automates performance testing on the Spine-Leaf topology.

        Test A (Balanced Load): Generating balanced traffic distributed across leaves and measuring the total aggregate bandwidth capacity.

        Test B (Bottleneck): Creating traffic patterns that intentionally cause a bottleneck on a single Leaf switch and analyzing the resulting performance drop.

    Final network architecture recommendations based on quantitative data according to specific company priorities (Performance-focused vs. Cost-focused).

Technologies and Tools Used

    Mininet: SDN and network topology emulator.

    Python: Topology construction and stress test automation (via Mininet Python API).

    iperf & ping & traceroute: Network performance, latency, and path analysis tools.

    TCLink: Traffic control, latency, and bandwidth limitations (75 Mbps/1ms host-to-switch, 100 Mbps/2ms switch-to-switch).

Repository Contents

    *.py files: Python scripts that build and launch the respective topologies on Mininet for each task.

    stress_test.py: The script that runs automated performance tests on the Spine-Leaf topology.

    Note: All test screenshots, measurement results, and theoretical calculations have been submitted separately as a PDF report.
