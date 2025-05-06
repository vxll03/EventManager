import styles from "./button.module.scss";

function Button({ children }) {
  return <button className={styles.button}>{children}</button>;
}

export default Button;
