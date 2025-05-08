import axios from "axios";

const URL = "http://localhost:8000/api/auth";

export const login = async (username, password) => {
  try {
    const response = await axios.post(
      `${URL}/login`,
      { username, password },
      {
        headers: { "Content-Type": "application/json" },
        withCredentials: true,
      }
    );
    return response.status;
  }
  catch(err) {
    console.log(`Ошибка: ${err.response.data}`);
    return err.response.status;
  }
};

export const register = async (username, password) => {
  try {
    const response = await axios.post(
      `${URL}/register`,
      { username, password },
      {
        headers: { "Content-Type": "application/json" },
        withCredentials: true,
      }
    );
    return response.status;
  }
  catch(err) {
    console.log(`Ошибка: ${err.response.data}`);
    return err.response.status;
  }
};
