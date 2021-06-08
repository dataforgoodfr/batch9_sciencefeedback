import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";

const Keywords = ({ data, onSubmit }) => {
  const { register, handleSubmit } = useForm();
  const [selected, setSelected] = useState(data);
  const [unselected, setUnselected] = useState([]);

  useEffect(() => {
    setSelected(data);
  }, [data]);

  const removeTag = (tag) => () => {
    setSelected(selected.filter((value) => value !== tag));
    setUnselected([...unselected, tag]);
  };

  const addTag = (tag) => () => {
    setUnselected(unselected.filter((value) => value !== tag));
    setSelected([...selected, tag]);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="keywords">
      Suggested keywords selected:
      <div className="select-zone">
        {selected.map((tag) => (
          <div className="tag" key={tag}>
            {tag}
            <button onClick={removeTag(tag)}>x</button>
          </div>
        ))}
      </div>
      Suggested keywords unselected:
      <div>
        <div className="select-zone">
          {unselected.map((tag) => (
            <div className="tag" key={tag}>
              {tag}
              <button onClick={addTag(tag)}>x</button>
            </div>
          ))}
        </div>
      </div>
      <input hidden {...register("search_query", { value: selected })} />
      <input type="submit" />
    </form>
  );
};

export default Keywords;
