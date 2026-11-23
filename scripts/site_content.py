"""Shared service, application and engagement copy for the site."""

# Slug, title, icon, short description.
SERVICES = (
    (
        "rtl-design-services", "Chip architecture & RTL design", "chip",
        "Turn a specification into digital logic, from block design and interfaces to integration.",
    ),
    (
        "verification-coverage-closure", "Design verification", "check",
        "Check that the design behaves as expected with simulation, debugging and coverage reviews.",
    ),
    (
        "fpga-prototyping-services", "FPGA prototyping", "board",
        "Run your design on reprogrammable hardware to check interfaces, timing and behaviour.",
    ),
    (
        "consultancy", "Engineering consultancy", "compass",
        "Get a technical review of requirements, design options or a decision your team needs to make.",
    ),
    (
        "ip-quality-audit", "IP review & integration", "layers",
        "Assess reusable design blocks, check interfaces and plan how to integrate them into your system.",
    ),
)

# Slug, title, icon, example, search terms.
APPLICATIONS = (
    ("compute", "Computing & infrastructure", "chip",
     "Hardware accelerators, data movement and platform integration.",
     "server data centre datacenter HPC"),
    ("security", "Security & trusted communications", "shield",
     "Cryptographic hardware, secure interfaces and post-quantum research.",
     "cryptography PQC secure connectivity protection encryption"),
    ("quantum", "Quantum technology & control", "signal",
     "Digital control, readout electronics and research instrumentation.",
     "control readout laboratory quantum computing"),
    ("edge-ai", "Edge AI & semiconductor products", "chip",
     "On-device processing, embedded accelerators and chip development.",
     "artificial intelligence inference vision ML ASIC"),
    ("industrial", "Industrial systems & mobility", "signal",
     "Industrial control, timing-sensitive interfaces and hardware-in-the-loop testing.",
     "automation automotive mobility power electronics factory motor HIL"),
    ("autonomous", "Autonomous & embedded systems", "board",
     "Digital hardware and interfaces for robotics and connected devices.",
     "robot embedded firmware robotics edge sensors"),
    ("space", "Space & mission technology", "orbit",
     "Subsystem interfaces and digital design for satellite or ground systems.",
     "space payload aerospace satellite ground station"),
    ("networks", "Networks & communications", "network",
     "Digital processing, integration and verification for wired or wireless platforms.",
     "telecom ethernet packet broadband connectivity wireless"),
    ("instrumentation", "Sensing & instrumentation", "signal",
     "Data acquisition, imaging, measurement and signal interfaces.",
     "sensor ADC DAC measurement instrumentation"),
    ("financial", "Financial technology infrastructure", "signal",
     "Data processing and hardware evaluation for latency-sensitive systems.",
     "fintech financial low latency market data"),
    ("processors", "Processors & open architectures", "chip",
     "Processor design blocks, interfaces and validation, including RISC-V systems.",
     "RISC-V RISCV CPU instruction set processor SoC"),
    ("engineering", "Engineering & design organisations", "layers",
     "Defined design tasks, independent reviews and support for integration teams.",
     "partner design house system integrator"),
    ("institutions", "Research & public programmes", "orbit",
     "Feasibility studies, prototypes and evaluation for universities and labs.",
     "academic institution research public government university laboratory"),
)

# Key, client-friendly title, scope and typical starting point.
MODELS = (
    ("consultancy", "Technical review",
     "A focused review of a design, requirement or engineering decision.",
     "Bring the decision you need to make and the options or constraints you already know."),
    ("project", "Defined project",
     "A deliverable with an agreed scope, responsibilities and review criteria.",
     "Bring a specification or a clear description of what you need delivered."),
    ("collaboration", "Joint development",
     "Shared engineering work with your team or research partners.",
     "Bring the project goals and the areas where you would like us to contribute."),
    ("ongoing", "Ongoing engineering support",
     "Support across multiple stages of a project, planned around your team’s workload.",
     "Bring your upcoming milestones, the skills you need and how you plan to work with us."),
)

# Service details keyed by the existing public route.
DETAILS = {
    "rtl-design-services": (
        "From chip architecture to digital logic",
        "Develop new digital blocks or extend an existing design. Register-transfer level (RTL) code defines how a digital circuit moves and processes data.",
        (
            ("Architecture", "Review requirements, data paths, interfaces and design constraints."),
            ("Digital logic", "Define the block and develop or review its RTL implementation."),
            ("Integration", "Review interface behaviour, clocks, resets and the handover to verification or system integration."),
        ),
        ("The function or interface you need", "The existing design, if any", "Performance, timing or integration constraints"),
    ),
    "verification-coverage-closure": (
        "Design verification",
        "Check the implementation against your specification and understand which behaviours still need testing.",
        (
            ("Verification plan", "Identify required behaviours, edge cases and ways to measure coverage."),
            ("Simulation & debugging", "Build or extend testbenches, run regressions and investigate failures."),
            ("Coverage review", "Review results, identify gaps and agree what evidence is needed for the next milestone."),
        ),
        ("The specification and interfaces", "Your simulator or verification environment", "Current coverage goals or difficult failures"),
    ),
    "fpga-prototyping-services": (
        "FPGA prototyping & hardware validation",
        "Use a field-programmable gate array (FPGA), a reprogrammable chip, to run a digital design and evaluate it on a board.",
        (
            ("Platform selection", "Review board options, resources, interfaces and timing constraints."),
            ("Implementation & bring-up", "Integrate the design, build the FPGA image and check that it runs on the target board."),
            ("Evaluation", "Run agreed tests and document results, limitations and follow-up work."),
        ),
        ("The target board or platform requirements", "The design and interfaces to test", "The behaviour or measurements you need to confirm"),
    ),
    "consultancy": (
        "Engineering consultancy",
        "Get a focused technical review before choosing an architecture, starting development or resolving a design problem.",
        (
            ("Feasibility", "Review requirements, assumptions and constraints to identify viable options."),
            ("Design review", "Examine architecture, interfaces or verification plans and identify areas that need attention."),
            ("Next steps", "Agree the questions to resolve, the evidence to gather and who will own each action."),
        ),
        ("The decision you need to make", "The constraints and options you already know", "The type of review or outcome you need"),
    ),
    "ip-quality-audit": (
        "Reusable IP review & integration",
        "Assess a reusable hardware design block, also called semiconductor IP, before integrating it into your system.",
        (
            ("Design review", "Check available documentation, interface specifications and verification evidence."),
            ("Interface fit", "Review data formats, timing, clock and reset behaviour and integration assumptions."),
            ("Integration plan", "Identify work needed to adapt the block, verify the integration and document any open issues."),
        ),
        ("The block and its intended use", "The interfaces and documentation you can describe", "Your integration stage and acceptance criteria"),
    ),
    "floating-point-ip": (
        "Floating-point & digital IP",
        "Discuss arithmetic hardware for compute and signal processing, including designs that use floating-point formats such as IEEE 754.",
        (
            ("Arithmetic requirements", "Define operations, data formats and rounding behaviour."),
            ("System fit", "Review interface, throughput and latency needs alongside the target platform."),
            ("Evaluation & integration", "Discuss test cases, comparison models and data-path integration."),
        ),
        ("The arithmetic function and data formats", "The target platform and interfaces", "Latency, throughput or accuracy goals"),
    ),
    "cryptographic-hardware-acceleration": (
        "Cryptographic hardware engineering",
        "Explore digital design, verification and prototyping for cryptographic hardware within an agreed research or development scope.",
        (
            ("Feasibility", "Discuss the intended use, relevant standards and evaluation requirements."),
            ("Architecture & integration", "Review hardware interfaces and the boundaries between the block and the rest of the system."),
            ("Prototype evaluation", "Define what the prototype should demonstrate and how results will be reviewed."),
        ),
        ("The non-confidential project objective", "Any applicable standards and evaluation requirements", "The hardware support you are looking for"),
    ),
    "research-to-hardware": (
        "From research to a hardware prototype",
        "Translate a research question into a digital design or prototype that you can test against agreed criteria.",
        (
            ("Feasibility & architecture", "Identify which assumptions matter and what can be evaluated on the target platform."),
            ("Prototype development", "Define a small, testable implementation and agree how teams will divide the work."),
            ("Evaluation & handover", "Plan the tests, document the results and discuss the next development step."),
        ),
        ("The research objective and current stage", "Existing models, measurements or prototypes", "What the next experiment needs to establish"),
    ),
    "semiconductor-design-partner-india": (
        "A semiconductor design partner in India",
        "Work with a Coimbatore-based engineering team on digital chip design, verification, FPGA prototypes and technical reviews.",
        (
            ("Project delivery", "Agree a defined engineering task, deliverables and review criteria."),
            ("Work alongside your team", "Define responsibilities, communication and handover across locations."),
            ("Supplier onboarding", "Discuss confidentiality, tool access, approved environments and procurement requirements."),
        ),
        ("Your project and the support you need", "Preferred working hours and review process", "Relevant onboarding or access requirements"),
    ),
}

# Keep these option values aligned with the existing enquiry service.
ENQUIRY_TYPES = (
    ("Service or consultancy discussion", "Engineering services or consultancy"),
    ("Schedule a meeting", "Request an introductory call"),
    ("Project collaboration", "Joint development project"),
    ("Research collaboration", "Research collaboration"),
    ("Supplier / partnership discussion", "Supplier or partnership enquiry"),
    ("Other requirement", "Other enquiry"),
)
