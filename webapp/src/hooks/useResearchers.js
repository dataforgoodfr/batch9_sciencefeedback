import { useState } from "react";

const mockData = {
  "C Carlos Chaccour": {
    score: 9,
    articles: [
      {
        doi: "http://doi.org/10.1186/s13063-020-04421-z",
        title:
          "The SaRS-CoV-2 Ivermectin Navarra-ISGlobal Trial (SaINT) to Evaluate the Potential of Ivermectin to Reduce COVID-19 Transmission in low risk, non-severe COVID-19 patients in the first 48 hours after symptoms onset: a structured summary of a study protocol for a randomized control pilot trial.",
        journal: "Trials",
        abstract:
          "The primary objective is to.....he placebo will not be visibly identical, but it will be administered by staff not involved in the clinical care or participant follow up.\nThe sample size is 24 patients: 12 participants will be randomised to the treatment group and 12 participants to the control group.\nCurrent protocol version: 1.0 dated 16 of april 2020. Recruitment is envisioned to begin by May 14th and end by June 14th.\nEudraCT number: 2020-001474-29, registered april 1",
        publication_date: "2020-06-10",
      },
      {
        doi: "http://doi.org/10.1016/j.eclinm.2020.100720",
        title:
          "The effect of early treatment with ivermectin on viral load, symptoms and humoral response in patients with non-severe COVID-19: a pilot, double-blind, placebo-controlled, randomized clinical trial.",
        journal: "EClinicalMedicine",
        abstract:
          "Ivermectin inhibits the replication of SaRS-CoV-2 in vitro at concentrations not readily achievable with currently approved doses. There is limited evidence to support its cl....obal Health and Clínica Universidad de Navarra.",
        publication_date: "2021-01-27",
      },
      {
        doi: "http://doi.org/10.1186/s13063-021-05236-2",
        title:
          "Randomized clinical trial to compare the efficacy of ivermectin versus placebo to negativize nasopharyngeal PCR in patients with early COVID-19 in Peru (SaINT-Peru): a structured summary of a study protocol for randomized controlled trial.",
        journal: "Trials",
        abstract:
          'The primary objective ....up.\nCurrent protocol version: 2.0 dated January 15\n"Ensayo Clínico aleatorizado de Fase IIa para comparar la efectividad de la ivermectina versus placebo en la negativización del PCR en pacientes en fase temprana de COVID-19" Peru National Health Institute REPEC with number: PER-034-20 , registered July 17',
        publication_date: "2021-04-11",
      },
    ],
    affiliation: [
      "Instituto de Salud Global de Barcelona, Barcelona, Spain. carlos.chaccour@isglobal.org.",
      "ISGlobal, Hospital Clínic",
      "Instituto de Salud Global (ISGlobal), Barcelona, Spain.\nFacultad de Medicina, Universidad de Navarra, Pamplona, Spain.",
    ],
  },
  "Da David a Jans": {
    score: 9,
    articles: [
      {
        doi: "http://doi.org/10.3390/cells9092100",
        title:
          "Ivermectin as a Broad-Spectrum Host-Directed antiviral: The Real Deal?",
        journal: "Cells",
        abstract:
          "The small molecule .... in progress worldwide for SaRS-CoV-2. This mini-review discusses the case for ivermectin as a host-directed broad-spectrum antiviral agent for a range of viruses, including SaRS-CoV-2.",
        publication_date: "2020-09-19",
      },
      {
        doi: "http://doi.org/10.1042/BST20200568",
        title: "antivirals that target the host IMPα/β1-virus interface.",
        journal: "Biochemical Society transactions",
        abstract:
          "although transport int....s a target for antiviral development.",
        publication_date: "2021-01-14",
      },
      {
        doi: "http://doi.org/10.1016/j.bbrc.2020.10.042",
        title:
          "The broad spectrum host-directed agent ivermectin as an antiviral for SaRS-CoV-2 ?",
        journal: "Biochemical and biophysical research communications",
        abstract:
          "FDa approved for parasitic indic....sults that are available, as well as those from observational/retrospective studies, indicate clinical benefit. Here we discuss the case for ivermectin as a host-directed broad-spectrum antiviral agent, including for SaRS-CoV-2.",
        publication_date: "2020-12-21",
      },
    ],
    affiliation: [
      "Nuclear Signaling Lab., Department of Biochemistry and Molecular Biology, Biomedicine Discovery Institute, Monash University, Monash, Victoria 3800, australia.",
      "Nuclear Signaling Lab., Department of Biochemistry and Molecular Biology, Biomedicine Discovery Institute, Monash University, Melbourne, australia.",
      "Nuclear Signaling Lab., Department of Biochemistry and Molecular Biology, Biomedicine Discovery Institute, Monash University, Melbourne, australia. Electronic address: David.Jans@monash.edu.",
    ],
  },
  "M Mika Turkia": {
    score: 5,
    articles: [
      {
        doi: "http://doi.org/10.7759/cureus.12403",
        title:
          "The History of Methylprednisolone, ascorbic acid, Thiamine, and Heparin Protocol and I-MaSK+ Ivermectin Protocol for COVID-19.",
        journal: "Cureus",
        abstract:
          "an alliance of established experts....D-19 and for treatment of all phases of COVID-19 including outpatient treatment of the early symptomatic phase. Therefore, at the end of October 2020, a separate ivermectin-based I-MaSK+ protocol for prophylaxis and early outpatient treatment of COVID-19 was published.",
        publication_date: "2021-02-04",
      },
      {
        doi: "http://doi.org/10.1080/13543784.2021.1901883",
        title: "The time to offer treatments for COVID-19.",
        journal: "Expert opinion on investigational drugs",
        abstract: "",
        publication_date: "2021-03-16",
      },
    ],
    affiliation: [
      "Qualitative Research, Independent Researcher, Helsinki, FIN.",
      "Qualitative Research, Helsinki, Finland.",
    ],
  },
  "E Emanuele Rizzo": {
    score: 4,
    articles: [
      {
        doi: "http://doi.org/10.1007/s00210-020-01902-5",
        title:
          "Ivermectin, antiviral properties and COVID-19: a possible new mechanism of action.",
        journal: "Naunyn-Schmiedeberg's archives of pharmacology",
        abstract:
          "Ivermectin is an antiparasitic drug that has shown also an effective pharmacological activity towards various infective agents, including viruses. This paper proposes an alternative mechanism of action for this drug that makes it capable of having an antiviral action, also against the novel coronavirus, in addition to the processes already reported in literature.",
        publication_date: "2020-05-29",
      },
    ],
    affiliation: [
      "Department of Prevention, Local Health authority of Lecce (aSL Lecce), Lecce, Italy. emanuele.rizzo@email.com.\nItalian Society of Environmental Medicine (SIMa), Milan, Italy. emanuele.rizzo@email.com.",
    ],
  },
  "R R Choudhary": {
    score: 4,
    articles: [
      {
        doi: "http://doi.org/10.1016/j.nmni.2020.100684",
        title:
          "Potential use of hydroxychloroquine, ivermectin and azithromycin drugs in fighting COVID-19: trends, scope and relevance.",
        journal: "New microbes and new infections",
        abstract:
          "alarming situation has....studied in detail individually and in combination in-vivo in order to combat COVID-19 infection.",
        publication_date: "2020-04-24",
      },
    ],
    affiliation: [
      "Department of Biotechnology, Maharishi Markandeshwar (Deemed to be University), Mullana ambala Haryana, India.",
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
