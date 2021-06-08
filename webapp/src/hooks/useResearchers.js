import { useState } from "react";

const mockData = {
  "C Carlos Chaccour": {
    Score: 9,
    Articles: [
      {
        doi: "http://doi.org/10.1186/s13063-020-04421-z",
        Title:
          "The SARS-CoV-2 Ivermectin Navarra-ISGlobal Trial (SAINT) to Evaluate the Potential of Ivermectin to Reduce COVID-19 Transmission in low risk, non-severe COVID-19 patients in the first 48 hours after symptoms onset: A structured summary of a study protocol for a randomized control pilot trial.",
        Journal: "Trials",
        Abstract:
          "The primary objective is to.....he placebo will not be visibly identical, but it will be administered by staff not involved in the clinical care or participant follow up.\nThe sample size is 24 patients: 12 participants will be randomised to the treatment group and 12 participants to the control group.\nCurrent protocol version: 1.0 dated 16 of April 2020. Recruitment is envisioned to begin by May 14th and end by June 14th.\nEudraCT number: 2020-001474-29, registered April 1",
        Publication_Date: "2020-06-10",
      },
      {
        doi: "http://doi.org/10.1016/j.eclinm.2020.100720",
        Title:
          "The effect of early treatment with ivermectin on viral load, symptoms and humoral response in patients with non-severe COVID-19: A pilot, double-blind, placebo-controlled, randomized clinical trial.",
        Journal: "EClinicalMedicine",
        Abstract:
          "Ivermectin inhibits the replication of SARS-CoV-2 in vitro at concentrations not readily achievable with currently approved doses. There is limited evidence to support its cl....obal Health and Clínica Universidad de Navarra.",
        Publication_Date: "2021-01-27",
      },
      {
        doi: "http://doi.org/10.1186/s13063-021-05236-2",
        Title:
          "Randomized clinical trial to compare the efficacy of ivermectin versus placebo to negativize nasopharyngeal PCR in patients with early COVID-19 in Peru (SAINT-Peru): a structured summary of a study protocol for randomized controlled trial.",
        Journal: "Trials",
        Abstract:
          'The primary objective ....up.\nCurrent protocol version: 2.0 dated January 15\n"Ensayo Clínico aleatorizado de Fase IIa para comparar la efectividad de la ivermectina versus placebo en la negativización del PCR en pacientes en fase temprana de COVID-19" Peru National Health Institute REPEC with number: PER-034-20 , registered July 17',
        Publication_Date: "2021-04-11",
      },
    ],
    Affiliation: [
      "Instituto de Salud Global de Barcelona, Barcelona, Spain. carlos.chaccour@isglobal.org.",
      "ISGlobal, Hospital Clínic",
      "Instituto de Salud Global (ISGlobal), Barcelona, Spain.\nFacultad de Medicina, Universidad de Navarra, Pamplona, Spain.",
    ],
  },
  "DA David A Jans": {
    Score: 9,
    Articles: [
      {
        doi: "http://doi.org/10.3390/cells9092100",
        Title:
          "Ivermectin as a Broad-Spectrum Host-Directed Antiviral: The Real Deal?",
        Journal: "Cells",
        Abstract:
          "The small molecule .... in progress worldwide for SARS-CoV-2. This mini-review discusses the case for ivermectin as a host-directed broad-spectrum antiviral agent for a range of viruses, including SARS-CoV-2.",
        Publication_Date: "2020-09-19",
      },
      {
        doi: "http://doi.org/10.1042/BST20200568",
        Title: "Antivirals that target the host IMPα/β1-virus interface.",
        Journal: "Biochemical Society transactions",
        Abstract:
          "Although transport int....s a target for antiviral development.",
        Publication_Date: "2021-01-14",
      },
      {
        doi: "http://doi.org/10.1016/j.bbrc.2020.10.042",
        Title:
          "The broad spectrum host-directed agent ivermectin as an antiviral for SARS-CoV-2 ?",
        Journal: "Biochemical and biophysical research communications",
        Abstract:
          "FDA approved for parasitic indic....sults that are available, as well as those from observational/retrospective studies, indicate clinical benefit. Here we discuss the case for ivermectin as a host-directed broad-spectrum antiviral agent, including for SARS-CoV-2.",
        Publication_Date: "2020-12-21",
      },
    ],
    Affiliation: [
      "Nuclear Signaling Lab., Department of Biochemistry and Molecular Biology, Biomedicine Discovery Institute, Monash University, Monash, Victoria 3800, Australia.",
      "Nuclear Signaling Lab., Department of Biochemistry and Molecular Biology, Biomedicine Discovery Institute, Monash University, Melbourne, Australia.",
      "Nuclear Signaling Lab., Department of Biochemistry and Molecular Biology, Biomedicine Discovery Institute, Monash University, Melbourne, Australia. Electronic address: David.Jans@monash.edu.",
    ],
  },
  "M Mika Turkia": {
    Score: 5,
    Articles: [
      {
        doi: "http://doi.org/10.7759/cureus.12403",
        Title:
          "The History of Methylprednisolone, Ascorbic Acid, Thiamine, and Heparin Protocol and I-MASK+ Ivermectin Protocol for COVID-19.",
        Journal: "Cureus",
        Abstract:
          "An alliance of established experts....D-19 and for treatment of all phases of COVID-19 including outpatient treatment of the early symptomatic phase. Therefore, at the end of October 2020, a separate ivermectin-based I-MASK+ protocol for prophylaxis and early outpatient treatment of COVID-19 was published.",
        Publication_Date: "2021-02-04",
      },
      {
        doi: "http://doi.org/10.1080/13543784.2021.1901883",
        Title: "The time to offer treatments for COVID-19.",
        Journal: "Expert opinion on investigational drugs",
        Abstract: "",
        Publication_Date: "2021-03-16",
      },
    ],
    Affiliation: [
      "Qualitative Research, Independent Researcher, Helsinki, FIN.",
      "Qualitative Research, Helsinki, Finland.",
    ],
  },
  "E Emanuele Rizzo": {
    Score: 4,
    Articles: [
      {
        doi: "http://doi.org/10.1007/s00210-020-01902-5",
        Title:
          "Ivermectin, antiviral properties and COVID-19: a possible new mechanism of action.",
        Journal: "Naunyn-Schmiedeberg's archives of pharmacology",
        Abstract:
          "Ivermectin is an antiparasitic drug that has shown also an effective pharmacological activity towards various infective agents, including viruses. This paper proposes an alternative mechanism of action for this drug that makes it capable of having an antiviral action, also against the novel coronavirus, in addition to the processes already reported in literature.",
        Publication_Date: "2020-05-29",
      },
    ],
    Affiliation: [
      "Department of Prevention, Local Health Authority of Lecce (ASL Lecce), Lecce, Italy. emanuele.rizzo@email.com.\nItalian Society of Environmental Medicine (SIMA), Milan, Italy. emanuele.rizzo@email.com.",
    ],
  },
  "R R Choudhary": {
    Score: 4,
    Articles: [
      {
        doi: "http://doi.org/10.1016/j.nmni.2020.100684",
        Title:
          "Potential use of hydroxychloroquine, ivermectin and azithromycin drugs in fighting COVID-19: trends, scope and relevance.",
        Journal: "New microbes and new infections",
        Abstract:
          "Alarming situation has....studied in detail individually and in combination in-vivo in order to combat COVID-19 infection.",
        Publication_Date: "2020-04-24",
      },
    ],
    Affiliation: [
      "Department of Biotechnology, Maharishi Markandeshwar (Deemed to be University), Mullana Ambala Haryana, India.",
    ],
  },
};

const useResearchers = (url, options) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchResearchers = async (params) => {
    const url = new URL("https://server.api");
    url.search = new URLSearchParams(params).toString();

    setIsLoading(true);
    try {
      // const resp = await fetch(url);
      // const data = await resp.json();

      const data = await new Promise((resolve) => {
        setTimeout(() => {
          resolve(mockData);
        }, 150);
      });

      setData(data);
    } catch (e) {
      setData([]);
      setError(e);
    }
    setIsLoading(false);

    return data;
  };

  return { data, error, isLoading, fetchResearchers };
};

export default useResearchers;
