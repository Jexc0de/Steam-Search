import styles from "./GameCard.module.css";

function GameCard({ title, year, rating, genre, image }) {
  return (
    <div className={styles.card}>
      <div className={styles.imageWrapper}>
        <img src={image} alt={title} className={styles.image} />
      </div>

      <div className={styles.text}>
        <p className={styles.title}>{title}</p>
        <p className={styles.meta}>
          {year} | {rating} | {genre}
        </p>
        <button className={styles.synopsisButton}>Synopsis ⬇</button>
      </div>
    </div>
  );
}

export default GameCard;