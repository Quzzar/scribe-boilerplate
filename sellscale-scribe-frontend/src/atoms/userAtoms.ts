import { atom } from "recoil";

const userDataState = atom({
  key: "user-data",
  default: JSON.parse(localStorage.getItem("user-data") ?? '{}') || {},
});

export {
  userDataState,
};
