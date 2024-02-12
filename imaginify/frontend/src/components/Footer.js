import { Link } from "react-router-dom";
import React from "react";
import classes from "./Footer.module.css";

const Footer = () => {
  return (
    <footer className={classes.footer}>
      <div className="grid grid-cols-3 gap-4 ">
        <ul className="p-4 flex flex-col items-center">
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/"> Register</Link>
          </li>
          <li>
            <Link to="/">Log In</Link>
          </li>
          <li>
            <Link to="/">Posts</Link>
          </li>
        </ul>

        <ul className="p-4 flex flex-col items-center">
          <li>
            <Link to="/">Instagram</Link>
          </li>
          <li>
            <Link to="/">LinkedIn</Link>
          </li>
          <li>
            <Link to="/">Twitter (X)</Link>
          </li>
          <li>
            <Link to="/">Facebook</Link>
          </li>
          <li>
            <Link to="/">Blog</Link>
          </li>
        </ul>
        <ul className="p-4 flex flex-col items-center">
          <li>
            <Link to="/">Docs</Link>
          </li>
          <li>
            <Link to="/">Cookie Preferences</Link>
          </li>
          <li>
            <Link to="/">Legal Notices</Link>
          </li>
        </ul>
      </div>
    </footer>
  );
};

export default Footer;
