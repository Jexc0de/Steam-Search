import styles from "./RecGrid.module.css";
import GameCard from "./GameCard";

function RecommendationGrid({ games }) {
  return (
    <div className={styles.grid}>
      {games.map((game) => (
        <GameCard key={game.id} {...game} />
      ))}
    </div>
  );
}

export default RecommendationGrid;
