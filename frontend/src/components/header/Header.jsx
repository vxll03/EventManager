import styles from "./header.module.scss";

import logo from "../../assets/img/logo_white.svg";
import sort from "../../assets/img/sorting.png";
import filter from "../../assets/img/filter.png";
import profile from "../../assets/img/house-door.png";
import { useNavigate } from "react-router-dom";

function Header() {
  const navigate = useNavigate()
  const handleLogin = () => {
    navigate("/auth")
  }
  const handleHome = () => {
    navigate("/")
  }

  return (
    <header className={styles.header}>
      <div className={styles.logo_container}>
        <img src={logo} alt="logo" onClick={handleHome}/>
      </div>

      <div className={styles.navigation}>
        <a href="#" className={styles.sort}>
          <img src={sort} />
          <span>Сортировка</span>
        </a>
        <a href="#" className={styles.filter}>
          <img src={filter} />
          <span>Фильтр</span>
        </a>
      </div>

      <div className={styles.profile}>
        <button onClick={handleLogin} className={styles.button}>
          <img src={profile} alt="Профиль" />
          <span>Войти</span>
        </button>
      </div>
    </header>
  );
}

export default Header;
