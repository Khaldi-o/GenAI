import React, { useState } from "react";
import { NavLink, Form, useRouteLoaderData, Link } from "react-router-dom";
import classes from "./MainNavigation.module.css";
import FujitsuLogo from "../assets/Fujitsu_Uvance_logo.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import Button from "./UI/Button";

function MainNavigation() {
  const token = useRouteLoaderData("root");
  const user_id = localStorage.getItem("id");
  const [isNavOpen, setIsNavOpen] = useState(false);

  const toggleNav = () => {
    setIsNavOpen(!isNavOpen);
  };

  const closeNav = () => {
    setIsNavOpen(false);
  };

  return (
    <header className={classes.header}>
      <img src={FujitsuLogo} alt="logo" className={classes.logo} />

      <div
        className={`${classes.hamburgerMenu} ${
          isNavOpen ? classes.reduce : ""
        }`}
        onClick={toggleNav}
      >
        <FontAwesomeIcon icon={faBars} />
      </div>

      <nav className={`${classes.navbar} ${isNavOpen ? classes.open : ""}`}>
        <ul className={classes.primaryNav}>
          <li>
            <NavLink
              to="/"
              className={({ isActive }) =>
                isActive ? classes.active : undefined
              }
              end
              onClick={closeNav}
            >
              Home
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/"
              className={({ isActive }) =>
                isActive ? classes.active : undefined
              }
              end
              onClick={closeNav}
            >
              Docs
            </NavLink>
          </li>
          <li>
            <NavLink
              to={"/history/" + user_id}
              className={({ isActive }) =>
                isActive ? classes.active : undefined
              }
              end
              onClick={closeNav}
            >
              Catalog
            </NavLink>
          </li>
        </ul>
      </nav>
      <div className={classes.login_button}>
        {!token && (
          <Link to="/auth?mode=login" className="tabs__link">
            <Button>Log In</Button>
          </Link>
        )}

        {token && (
          <Form action="/logout" method="post">
            <Button> Logout </Button>
          </Form>
        )}
      </div>
    </header>
  );
}

export default MainNavigation;
