import { useForm } from "react-hook-form";

const SearchBar = ({ onSubmit }) => {
  const { register, handleSubmit, watch } = useForm({
    defaultValues: {
      max_distance: 1,
    },
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label htmlFor="searchbar">Search</label>
      <input {...register("search_query", { required: true })} />

      <label htmlFor="max_distance">{watch("max_distance")}</label>
      <input
        type="range"
        min="1"
        max="5"
        step="0.1"
        defaultValue={1}
        {...register("max_distance", { required: true })}
      />
      <input type="submit" />
    </form>
  );
};

export default SearchBar;
