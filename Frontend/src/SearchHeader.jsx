import styles from "./SearchHeader.module.css";

function SearchBar({placeholder}) {
  return (
    <div className={styles.searchContainer}>
      <input type="text" placeholder={placeholder} className={styles.input} />
      <button className={styles.iconBtn}>🔍</button>
    </div>
  );
}

export default SearchBar;