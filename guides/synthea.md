# Synthea

> Generate synthetic patient lifespans with diseases, encounters, medications and procedures, and write them as CSV tables.

Licence: Apache-2.0 · [Source code](https://github.com/synthetichealth/synthea)

## What it simulates

Synthea simulates the lives of synthetic people from birth to death or to a reference date. Each person is moved through disease modules (state machines written as JSON) that decide diagnoses, visits, medications, procedures, immunizations and care plans. The output is a synthetic health record for each person, with no real patient behind it.

Demographics come from US census data for the state you choose. Disease onset and progression come from published incidence and prevalence figures built into the modules.

Synthea is a record generator. It does not model transmission between people or the spread of an epidemic.

## When to use it

- You need realistic-looking patient tables to test an EHR pipeline, a database schema or an analytics query, and real records are off limits.
- You want a cohort with set properties, such as women aged 60 to 90 in Texas, to teach cohort queries.
- You want to see which conditions and encounters a care pathway produces over a decade.

Use [epydemix](epydemix.md) when the question is how an infectious disease spreads through a population. Synthea records are plausible, not validated for estimating real prevalence or for training clinical models without checks.

## Install it yourself

Synthea needs a Java runtime. The recipe uses Temurin 17 and the release jar from GitHub:

```
curl -L -o synthea-with-dependencies.jar \
  https://github.com/synthetichealth/synthea/releases/download/v4.0.0/synthea-with-dependencies.jar
java -jar synthea-with-dependencies.jar -p 10 -s 42 -r 20240101 --exporter.csv.export=true Massachusetts
```

The jar is 201 MB. By default the output goes to an `output/` folder next to where you run it.

## Run the tested example

This recipe builds Synthea in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 16.1 s.

1. Download [synthea-recipe.tar.gz](https://biosimhub.pages.dev/guides/synthea/synthea-recipe.tar.gz) (Dockerfile, run_synthea.sh, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf synthea-recipe.tar.gz
   cd synthea
   sh run.sh
   ```

![Terminal recording of the Synthea example run](https://biosimhub.pages.dev/media/synthea/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/synthea:4.0.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/synthea:4.0.0 /opt/run_synthea.sh 10 42 Massachusetts any 0 90 10 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `conditions.csv` | 96.9 KB |
| `encounters.csv` | 461.5 KB |
| `immunizations.csv` | 26.5 KB |
| `medications.csv` | 327.9 KB |
| `patients.csv` | 3.4 KB |
| `procedures.csv` | 529.9 KB |
| `run_log.txt` | 129 B |
| `summary.csv` | 124 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/synthea/result-dark.png"><img src="https://biosimhub.pages.dev/media/synthea/result.png" alt="Plot of the Synthea example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>conditions.csv</code></summary>

```
START,STOP,PATIENT,ENCOUNTER,SYSTEM,CODE,DESCRIPTION
1962-10-20,2022-10-08,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-c321-d9cc4b8b117e,SNOMED-CT,5689008,Chronic periodontitis
1975-12-27,,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-d26c-5188e7cb128d,SNOMED-CT,473461003,Educated to high school level (finding)
1990-04-27,,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-6a96-4f5ea0df8bb5,SNOMED-CT,82423001,Chronic pain (finding)
1990-06-03,,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-4817-49ab33862a3c,SNOMED-CT,196416002,Impacted molars (disorder)
1991-08-27,,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-9620-4cfbafa077fc,SNOMED-CT,124171000119105,Chronic intractable migraine without aura (disorder)
1992-07-25,,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-eb74-0148b8c3a330,SNOMED-CT,6525002,Dependent drug abuse (disorder)
1996-01-17,,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-7618-ad9115cbce12,SNOMED-CT,161744009,Past pregnancy history of miscarriage (situation)
1997-11-08,,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-516b-c9d956df9ac6,SNOMED-CT,59621000,Essential hypertension (disorder)
1997-11-
```

</details>

<details><summary>First lines of <code>encounters.csv</code></summary>

```
Id,START,STOP,PATIENT,ORGANIZATION,PROVIDER,PAYER,ENCOUNTERCLASS,CODE,DESCRIPTION,BASE_ENCOUNTER_COST,TOTAL_CLAIM_COST,PAYER_COVERAGE,REASONCODE,REASONDESCRIPTION
ba419d35-0dfe-8af7-c321-d9cc4b8b117e,1962-10-20T19:24:59Z,1962-10-20T20:06:49Z,ba419d35-0dfe-8af7-347c-eebf02485a56,a6964d47-8af0-3df2-b99d-d8414eb1cfa3,1e7e6183-8666-3962-99a3-2f0f98b9df7e,df166300-5
ba419d35-0dfe-8af7-d26c-5188e7cb128d,1975-12-27T19:24:59Z,1975-12-27T20:16:06Z,ba419d35-0dfe-8af7-347c-eebf02485a56,4705a8fd-19cd-32c1-8b3e-34bcfe84d0bd,95e71205-f63b-3e56-adf3-99bc2c9f4550,df166300-5
ba419d35-0dfe-8af7-6a96-4f5ea0df8bb5,1990-04-27T19:24:59Z,1990-04-27T20:24:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,d9b71ccf-6649-3555-9e99-44eac0af257f,34922409-94c7-325c-bf31-779939af18f5,df166300-5
ba419d35-0dfe-8af7-4817-49ab33862a3c,1990-06-03T19:24:59Z,1990-06-03T20:24:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,d9b71ccf-6649-3555-9e99-44eac0af257f,34922409-94c7-325c-bf31-779939af18f5,df166300-5
ba419d35-0dfe-8af7-9620-4cfbafa077fc,1991-08-27T19:24:59Z,1991-08-27T20:24:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,d9b71ccf-6649-3555-9e99-44eac0af257f,34922409-94c7-325c-bf31-779939af18f5,df166300-5
ba419d35-0dfe-8af7-ec19-86b4d2c1
```

</details>

<details><summary>First lines of <code>immunizations.csv</code></summary>

```
DATE,PATIENT,ENCOUNTER,CODE,DESCRIPTION,BASE_COST
2017-05-27T19:24:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-6390-07cc3d08a1c5,140,Influenza  split virus  trivalent  PF,136.00
2018-07-21T19:24:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-f26e-3dc41eb130a9,140,Influenza  split virus  trivalent  PF,136.00
2019-02-16T19:24:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-94f1-84b587dffeb7,113,Td (adult)  5 Lf tetanus toxoid  preservative free  adsorbed,136.00
2019-05-18T19:24:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-2841-d31234aada18,140,Influenza  split virus  trivalent  PF,136.00
2020-05-09T19:24:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-2d30-27549aae7c43,140,Influenza  split virus  trivalent  PF,136.00
2021-04-03T19:24:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-c4ea-bbb6124a2b69,207,COVID-19  mRNA  LNP-S  PF  100 mcg/0.5mL dose or 50 mcg/0.25mL dose,136.00
2021-05-01T19:24:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-a93d-6b0e3f0c0198,207,COVID-19  mRNA  LNP-S  PF  100 mcg/0.5mL dose or 50 mcg/0.25mL dose,136.00
2021-05-08T19:24:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,b
```

</details>

<details><summary>First lines of <code>medications.csv</code></summary>

```
START,STOP,PATIENT,PAYER,ENCOUNTER,CODE,DESCRIPTION,BASE_COST,PAYER_COVERAGE,DISPENSES,TOTALCOST,REASONCODE,REASONDESCRIPTION
2006-09-29T19:24:59Z,2018-04-30T19:24:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,df166300-5a78-3502-a46a-832842197811,ba419d35-0dfe-8af7-81d0-55d240114f01,849574,Naproxen sodium 220 MG Oral Tablet,168.1
2012-02-04T19:24:59Z,,ba419d35-0dfe-8af7-347c-eebf02485a56,df166300-5a78-3502-a46a-832842197811,ba419d35-0dfe-8af7-11b1-bb5d1838a57e,309362,Clopidogrel 75 MG Oral Tablet,173.59,123.59,179,31072.61,,
2012-02-04T19:24:59Z,,ba419d35-0dfe-8af7-347c-eebf02485a56,df166300-5a78-3502-a46a-832842197811,ba419d35-0dfe-8af7-11b1-bb5d1838a57e,312961,Simvastatin 20 MG Oral Tablet,159.61,109.61,179,28570.19,,
2012-02-04T19:24:59Z,,ba419d35-0dfe-8af7-347c-eebf02485a56,df166300-5a78-3502-a46a-832842197811,ba419d35-0dfe-8af7-11b1-bb5d1838a57e,866412,24 HR metoprolol succinate 100 MG Extended Release Oral Tabl
2012-02-04T19:24:59Z,,ba419d35-0dfe-8af7-347c-eebf02485a56,df166300-5a78-3502-a46a-832842197811,ba419d35-0dfe-8af7-11b1-bb5d1838a57e,705129,Nitroglycerin 0.4 MG/ACTUAT Mucosal Spray,15.44,0.00,179,276
2016-10-01T19:24:59Z,2016-11-05T19:24:59Z,ba419d35-0dfe-8af7-347c-eebf024
```

</details>

<details><summary>First lines of <code>patients.csv</code></summary>

```
Id,BIRTHDATE,DEATHDATE,SSN,DRIVERS,PASSPORT,PREFIX,FIRST,MIDDLE,LAST,SUFFIX,MAIDEN,MARITAL,RACE,ETHNICITY,GENDER,BIRTHPLACE,ADDRESS,CITY,STATE,COUNTY,FIPS,ZIP,LAT,LON,HEALTHCARE_EXPENSES,HEALTHCARE_CO
ba419d35-0dfe-8af7-347c-eebf02485a56,1957-11-02,,999-49-6110,S99942335,X20929998X,Ms.,Corie618,Sofia418,Jast432,,,S,white,nonhispanic,F,Chelmsford  Massachusetts  US,1028 Hoeger Crossroad,Franklin,Mas
aee7bbe1-0c45-c028-1e62-1f4cdb30c273,1980-06-03,,999-21-5544,S99958992,X30688173X,Mr.,Wilfredo622,Isaiah615,Fritsch593,,,M,white,nonhispanic,M,New Bedford  Massachusetts  US,265 Schamberger Rapid Unit
4f083ce3-f12b-bb4b-7353-e17f0cd55b0a,1959-04-12,,999-78-6352,S99941158,X72377557X,Mr.,Ezekiel373,Leslie90,Walter473,,,S,white,nonhispanic,M,Onset  Massachusetts  US,332 Schulist Underpass,Watertown,Ma
46ee9d82-b52c-856d-069b-5064ff052225,1937-11-20,,999-44-2741,S99953338,X6052585X,Mrs.,Shalanda398,Kelsie51,Herman763,,Terry864,W,white,nonhispanic,F,Marlborough  Massachusetts  US,925 Brown Annex,Lowe
aa616abe-1761-0c9a-7959-07544679dafd,2017-06-20,,999-83-4774,,,,Jona712,Bonnie873,Robel940,,,,asian,nonhispanic,F,Hanoi  Hà Đông  VN,997 Grant Row Unit 85,Peabody,Massachusetts,Essex County,25009
```

</details>

<details><summary>First lines of <code>procedures.csv</code></summary>

```
START,STOP,PATIENT,ENCOUNTER,SYSTEM,CODE,DESCRIPTION,BASE_COST,REASONCODE,REASONDESCRIPTION
2016-11-05T19:24:59Z,2016-11-05T19:39:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-b1ce-f449ddeb622f,SNOMED-CT,430193006,Medication reconciliation (procedure),456.43,,
2016-11-05T19:24:59Z,2016-11-05T20:15:40Z,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-b1ce-f449ddeb622f,SNOMED-CT,710824005,Assessment of health and social care needs (procedure),431.40,,
2016-11-05T20:15:40Z,2016-11-05T20:26:58Z,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-b1ce-f449ddeb622f,SNOMED-CT,171207006,Depression screening (procedure),431.40,,
2016-11-05T20:26:58Z,2016-11-05T20:54:01Z,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-b1ce-f449ddeb622f,SNOMED-CT,171207006,Depression screening (procedure),431.40,,
2016-12-24T19:24:59Z,2016-12-24T19:39:59Z,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-c36c-e291b2168a0d,SNOMED-CT,430193006,Medication reconciliation (procedure),777.59,,
2016-12-24T19:24:59Z,2016-12-24T20:19:49Z,ba419d35-0dfe-8af7-347c-eebf02485a56,ba419d35-0dfe-8af7-c36c-e291b2168a0d,SNOMED-CT,710824005,Assessment of health and social care needs (proced
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
Running with options:
Population: 10
Seed: 42
Location: Massachusetts
Min Age: 0
Max Age: 90
Records: total=11, alive=10, dead=1
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
table,rows
patients,11
encounters,1411
conditions,685
medications,1277
procedures,2757
immunizations,194
observations,19609
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `population` | Living patients to generate | 10 | 1 to 100 |
| `state` | US state | Massachusetts | Massachusetts, California, Texas, New York, Florida, Washington |
| `gender` | Gender | any | any, F, M |
| `min_age` | Minimum age | 0 | 0 to 140 |
| `max_age` | Maximum age | 90 | 0 to 140 |
| `years` | Years of history exported | 10 | 1 to 100 |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's script `run_synthea.sh` calls the jar with your options, then copies six CSV tables and a summary to the output folder. It turns off FHIR and the hospital and practitioner exports, sets a clinician seed equal to your seed, and fixes the reference date at 2024-01-01 so ages do not drift with the wall clock.

The default asks for 10 living patients (`-p 10`), seed 42, Massachusetts, ages 0 to 90, 10 years of history.

- `run_log.txt` ends with "Records: total=11, alive=10, dead=1". Synthea keeps generating until it has the requested number of living patients. People who die along the way are also written.
- `patients.csv` has 11 rows and 28 columns, including `BIRTHDATE`, `DEATHDATE`, `RACE`, `GENDER`, `CITY`, `INCOME`. The living patients are aged 4.7 to 86.1 years on the reference date, and one patient died in 2007.
- `encounters.csv` has 1,411 rows with `ENCOUNTERCLASS`, costs and a reason. 889 are ambulatory, 184 outpatient, 172 wellness and 78 urgent care.
- `conditions.csv` has 685 rows, `medications.csv` 1,277, `procedures.csv` 2,757 and `immunizations.csv` 194. Each row carries a `PATIENT` id that joins to `patients.csv`.
- `summary.csv` lists row counts per table. It also counts `observations` (19,609 rows), which the recipe does not return because of size.

The conditions table includes findings such as employment status and "Medication review due" as well as diseases. Filter on "(disorder)" to see diagnoses. In the default run the most common disorder is gingivitis (44 rows), then viral sinusitis (15), overdose (8) and acute viral pharyngitis (7). Four of the 11 patients have essential hypertension.

## Your own runs

Same recipe, the default settings except the stated option.

- **Another seed.** `seed 43` gave 10 records with no deaths, 701 encounters, 437 conditions and 981 medications. The default seed gave 11 records and 1,411 encounters. A different seed is a different cohort.
- **Older women.** `gender F`, ages 60 to 90, 30 patients gave 56 records (26 died), 5,681 encounters and 2,794 conditions. The mean age of the living was 75.1 years. Essential hypertension appeared for 21 of the 56 records, against 4 of 11 in the default run. Ischemic heart disease appeared 28 times.
- **Larger cohort in California.** 100 patients with `state California` gave 136 records (36 dead), 13,108 encounters and 6,383 conditions. The most common conditions were still "Medication review due" (1,330 rows) and stress (551 rows).
- **Reproducibility.** Two runs with the default settings gave identical row counts for all seven tables. The row order inside `patients.csv` differed between the two runs, so compare by patient id, not by line.

## Pitfalls

- **Dead patients inflate the count.** `-p` is the number of living patients. The table has more rows than that when people died in the simulated history.
- **Row order is not stable.** Generation is multithreaded. Sort by `Id` before diffing files.
- **Reference date matters.** Without `-r`, Synthea uses the current time as the end of the simulation, so ages and the set of living patients change from day to day. The recipe fixes it at 2024-01-01.
- **Age range and cohort size interact.** A narrow age range with a high minimum age leads to many more dead records than living ones, as the 60 to 90 run shows (26 of 56).
- **Not real data.** Names and SSNs in `patients.csv` are generated. Do not mix the tables with real records without labelling them.

## Further reading

- Source and wiki: https://github.com/synthetichealth/synthea
- Releases: https://github.com/synthetichealth/synthea/releases
- Paper: Walonoski J et al. (2018) Synthea: An approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record. J Am Med Inform Assoc 25:230-238. https://doi.org/10.1093/jamia/ocx079

---

Cite: Walonoski J, et al. (2018). Synthea: An approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record. J Am Med Inform Assoc 25:230-238. doi:10.1093/jamia/ocx079

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/synthea).
