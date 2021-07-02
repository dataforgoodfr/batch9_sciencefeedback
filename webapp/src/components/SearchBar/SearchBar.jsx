import { useForm } from "react-hook-form";
import { FiSearch } from "react-icons/fi";


import './searchBar.css'

const SearchBar = ({ onSubmit }) => {
    const { register, handleSubmit, watch } = useForm({
        defaultValues: {
            min_score: 1,
        },
    });

    return (
        <form className="searchbar" onSubmit={handleSubmit(onSubmit)}>
            <label className="searchbar-label" htmlFor="searchbar">Find experts on</label>

            <div className="searchbar-input">
                <FiSearch size={23} />
                <input {...register("search_query", { required: true })} />
            </div>

            <label htmlFor="min_score">{watch("min_score")}</label>
            <input
                type="range"
                min="1"
                max="10"
                step="0.1"
                defaultValue={1}
                {...register("min_score", { required: true })}
            />
            <input type="submit" value="Search" />
        </form>
    );
};

export default SearchBar;
