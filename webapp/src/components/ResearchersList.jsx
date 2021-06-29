const ResearchersList = ({ data }) => (
  <div className="reseachers-list">
    {data &&
      Object.keys(data).map((researcher) => (
        <span key={researcher}>{researcher}</span>
      ))}
  </div>
);

export default ResearchersList;
