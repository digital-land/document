#!/usr/bin/env python3
import re
import csv
import json
from pathlib import Path

e = re.compile(r"[^A-Za-z0-9]")

site="https://www.digital-land.info/"
dataset = Path().cwd().name
print("dataset:", dataset)

organisation_slug = {}
for row in csv.DictReader(open("../entity-builder/var/cache/organisation.csv")):
    organisation_slug[row["entity"]] = row["organisation"].replace(":", "/")

def redirect(path, to):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write('<meta http-equiv="refresh" content="0; url=%s%s">' % (site, to))


redirect("./docs/index.html", "dataset/%s" % dataset)

with open("docs/.nojekyll", 'w') as f: f.write('')

for row in csv.DictReader(open("../entity-builder/dataset/entity.csv")):
    if row["dataset"] != dataset:
        continue

    #path = Path("./docs/%s/%s/index.html" % (dataset, row["reference"]))
    #path = Path("./docs/%s/%s/index.html" % (organisation_slug[row["organisation-entity"]], reference))

    reference = e.sub("-", row["reference"])
    fields = json.loads(row["json"])

    path = Path("./docs/%s/%s/index.html" % (fields["document-types"], reference))
    redirect(path, "entity/" + row["entity"])
