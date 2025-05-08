import styles from "./register.module.scss";

function Register({ onToggleAuth, setUser, setPass, authenticate }) {
  return (
    <div className={styles.container}>
      <h1>Регистрация</h1>
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
          value="Зарегистрироваться"
          className={styles.button}
          onClick={authenticate}
        />
      </form>
      <p onClick={onToggleAuth}>Авторизоваться</p>
    </div>
  );
}

export default Register;
