// Search.js

import React from 'react';

function SearchBar(props) {

    return (
        <div className="card mb-3">
          <div className="mt-3"></div>
            <h4 align='left'>Search</h4>
          <div className="card-body">
            <input
              className="form-control"
              value={props.searchQuery}
              onChange={(e) => props.setSearchQuery(e.target.value)}
            />
            <div className="mt-3"></div>
            <button className="btn btn-primary mr-2" onClick={() => {
                  props.translate(props.searchQuery);
                  props.setShowQuery(true);
            }}>
              Search
            </button>

            <button className="btn btn-secondary" onClick={() => {
              props.setSearchQuery("");
              props.setShowQuery(false);
              props.setTranslatedQuery("")
            }}>
              Reset
            </button>
          </div>
        </div>
    )
}

export default SearchBar;