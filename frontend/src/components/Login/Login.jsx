import styles from "./login.module.scss";

function Login({ onToggleAuth, setUser, setPass, authenticate }) {
  return (
    <div className={styles.container}>
      <h1>Вход</h1>
      <form className={styles.form}>
        <label htmlFor="name">Имя пользователя</label>
        <input
          type="text"
          name="name"
          required
          minLength={4}
          maxLength={100}
          className={styles.input}
          onChange={(e) => setUser(e.target.value)}
        />

        <label htmlFor="pass">Пароль</label>
        <input
          type="password"
          name="pass"
          required
          minLength={8}
          maxLength={100}
          className={styles.input}
          onChange={(e) => setPass(e.target.value)}
        />

        <input
          type="button"
          value="Войти"
          className={styles.button}
          onClick={authenticate}
        />
      </form>
      <p onClick={onToggleAuth}>Зарегистрироваться</p>
    </div>
  );
}

export default Login;
