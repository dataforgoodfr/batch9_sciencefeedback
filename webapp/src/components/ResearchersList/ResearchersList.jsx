import Researcher from './Researcher'
import './researchersList.css'

const ResearchersList = ({ data }) => (
  <div className="researchers-list">
    <div className="researchers-list-title">
    <span className="researchers-list-number">{Object.keys(data).length}</span> Experts on Covid
    </div>
    {data &&
      Object.keys(data).map((researcher) => (
          <Researcher
            data={data[researcher]}
            key={researcher}
            name={researcher}
          />
      ))}
  </div>
);

export default ResearchersList;
