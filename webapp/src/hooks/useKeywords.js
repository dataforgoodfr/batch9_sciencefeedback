import { useState } from "react";

const mockData = ["ivermectin","ivermectina","liquiritigenin and glabridin","citoquine storm","mycoplasma igm","azitromicina","lumiradx antigen test"]

const useKeywords = (url, options) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchKeywords = async (params) => {
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

  return { data, error, isLoading, fetchKeywords };
};

export default useKeywords;
