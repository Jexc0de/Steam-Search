import styles from "./SelectedGameDisplay.module.css";

function MainFeaturedGame({ image }) {
  return (
    <div className={styles.container}>
      <img src={image} alt="Featured game" className={styles.image} />
    </div>
  );
}

export default MainFeaturedGame;