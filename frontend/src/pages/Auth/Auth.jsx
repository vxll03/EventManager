import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import toast, { Toaster } from "react-hot-toast";

import { login, register } from "../../routes/Auth";
import Login from "../../components/Login/Login";
import Register from "../../components/Register/Register";

import back from "../../assets/img/back.png";
import styles from "./auth.module.scss";

function Auth() {
  // true - Login, false - Register
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const toggleAuth = () => {
    setIsLogin(!isLogin);
    setPassword("");
    setUsername("");
  };

  const authenticate = async () => {
    if (isLogin) {
      const response = await login(username, password);
      if (response == 404) {
        toast.error("Неправильный логин или пароль");
        return;
      }
      toast.success("Успешный вход");

      navigate("/", { replace: true });
    } else {
      const response = await register(username, password);
      if (response == 400) {
        toast.error("Пользователь уже существует");
        return;
      }
      if (response == 422) {
        toast.error("Некорректные данные");
        return;
      }
      toast.success("Успешная регистрация");
      setIsLogin(true);
    }
  };

  return (
    <>
      <div>
        <Toaster position="bottom-center" />
      </div>

      <div className={styles.container}>
        <Link to="/" className={styles.link}>
          <img src={back} alt="На главную" />
        </Link>

        {isLogin ? (
          <Login
            onToggleAuth={toggleAuth}
            setPass={setPassword}
            setUser={setUsername}
            authenticate={authenticate}
          />
        ) : (
          <Register
            onToggleAuth={toggleAuth}
            setPass={setPassword}
            setUser={setUsername}
            authenticate={authenticate}
          />
        )}
      </div>
    </>
  );
}

export default Auth;
