import json
import random
from pathlib import Path

OUTPUT = Path("../data/incidents.json")

TECHNOLOGIES = [
    "Enterprise Server",
    "Visual COBOL",
    "Runtime",
    "CICS",
    "VSAM",
    "DB2",
    "Batch",
    "JCL",
    "Compiler",
    "Deployment"
]

ENVIRONMENTS = [
    "DEV",
    "SIT",
    "UAT",
    "PROD"
]

SEVERITIES = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

APPLICATIONS = [
    "Retail Banking",
    "Loan Processing",
    "Payments",
    "Insurance",
    "Credit Cards"
]

INCIDENT_LIBRARY = [

{
"title":"COBRT114 Runtime Error",
"technology":"Runtime",

"symptoms":[
"COBRT114",
"Runtime initialization failed",
"Application terminated"
],

"causes":[
"Incorrect COBDIR",
"Mixed runtime versions",
"Corrupted runtime libraries",
"Incorrect COBPATH"
],

"commands":[
"echo $COBDIR",
"echo $COBPATH",
"env | grep COB",
"cob -V"
],

"resolutions":[
"Update COBDIR",
"Update COBPATH",
"Restart Enterprise Server",
"Reinstall runtime"
]
},

{
"title":"File Status 39",

"technology":"VSAM",

"symptoms":[
"File Status 39",
"OPEN failed",
"Invalid file definition"
],

"causes":[
"FD mismatch",
"Incorrect record length",
"Catalog mismatch",
"Wrong organization"
],

"commands":[
"ls -lrt",
"cat file.def",
"file filename"
],

"resolutions":[
"Correct FD",
"Rebuild file",
"Update catalog",
"Redeploy dataset"
]
},

{
"title":"Enterprise Server Region Startup Failure",

"technology":"Enterprise Server",

"symptoms":[
"Region unavailable",
"ES region failed",
"Listener not started"
],

"causes":[
"License issue",
"Port already used",
"Configuration corruption",
"Runtime mismatch"
],

"commands":[
"mfesdi",
"netstat -an",
"systemctl status es"
],

"resolutions":[
"Restart region",
"Correct configuration",
"Update license",
"Free occupied port"
]
},

{
"title":"DB2 SQLCODE -911",

"technology":"DB2",

"symptoms":[
"Transaction rollback",
"Deadlock detected"
],

"causes":[
"Deadlock",
"Lock timeout",
"Long transaction"
],

"commands":[
"db2 list applications",
"db2pd"
],

"resolutions":[
"Retry transaction",
"Commit frequently",
"Reduce lock duration"
]
},

{
"title":"Batch Job RC12",

"technology":"Batch",

"symptoms":[
"Return Code 12",
"Batch failed"
],

"causes":[
"Dataset missing",
"JCL syntax",
"Program abend"
],

"commands":[
"cat job.log",
"grep RC job.log"
],

"resolutions":[
"Correct dataset",
"Fix JCL",
"Redeploy program"
]
}

]

def generate_incident(number):

    base = random.choice(INCIDENT_LIBRARY)

    cause = random.choice(base["causes"])

    return {

        "id": f"INC-{number:04}",

        "title": base["title"],

        "technology": base["technology"],

        "severity": random.choice(SEVERITIES),

        "environment": random.choice(ENVIRONMENTS),

        "application": random.choice(APPLICATIONS),

        "migration_phase": random.choice([
            "Assessment",
            "Conversion",
            "Compilation",
            "Deployment",
            "Post Deployment",
            "Production Support"
        ]),

        "frequency": random.choice([
            "Common",
            "Occasional",
            "Rare"
        ]),

        "symptoms": base["symptoms"],

        "business_impact":[

            "Application unavailable",

            "Migration delayed",

            "Batch execution failed"

        ],

        "logs":[

            random.choice(base["symptoms"]),

            cause

        ],

        "possible_root_causes": base["causes"],

        "actual_root_cause": cause,

        "diagnostic_commands": base["commands"],

        "resolution_steps": base["resolutions"],

        "validation":[

            "Application started",

            "No runtime errors",

            "Regression tests passed"

        ],

        "prevention":[

            "Deployment checklist",

            "Runtime validation",

            "Environment verification"

        ],

        "related_ibm_docs":[

            "COBOL Programming Guide",

            "Migration Guide"

        ],

        "related_microfocus_docs":[

            "Enterprise Server Administration Guide",

            "Runtime Configuration Guide"

        ],

        "keywords":[

            base["technology"],

            cause,

            base["title"]

        ]
    }

def main():

    incidents=[]

    NUMBER_OF_INCIDENTS=200

    for i in range(1,NUMBER_OF_INCIDENTS+1):

        incidents.append(

            generate_incident(i)

        )

    OUTPUT.parent.mkdir(

        exist_ok=True

    )

    with open(

        OUTPUT,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            incidents,

            f,

            indent=4

        )

    print()

    print("="*50)

    print("Synthetic Incident Dataset Created")

    print("="*50)

    print(f"Incidents : {len(incidents)}")

    print(f"Location  : {OUTPUT.resolve()}")

    print("="*50)

if __name__=="__main__":

    main()
