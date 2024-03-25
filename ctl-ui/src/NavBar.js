import React from "react";
import { Link } from "react-router-dom";
function Navbar() {
    return (<nav>
        <ul>
            <li>
                <Link to="/">Login</Link>
            </li>
            <li>
                <Link to="/createaccount">Create Account</Link>
            </li>
            <li>
                <Link to="/blah">Test Page Not Found</Link>
            </li>
        </ul>
    </nav>);
}

export default Navbar;