import React from 'react';
import useSearchTranslate from '../util/useSearchTranslate';
import SearchBar from './SearchBar';
import QueryDisplay from './QueryDisplay';
import GraphDisplay from './GraphDisplay';


function MainContent(){
    const {
       searchQuery,
        showQuery,
        translatedQuery,
        translate,
        setSearchQuery,
        setTranslatedQuery,
        setShowQuery
      } = useSearchTranslate();
    return (
      <div className="col-md-8">
        <div className="col-md-8"></div>
        <SearchBar showQuery={showQuery} searchQuery={searchQuery} setSearchQuery={setSearchQuery} translate={translate} setShowQuery={setShowQuery} setTranslatedQuery={setTranslatedQuery} />
        <QueryDisplay translatedQuery={translatedQuery} showQuery={showQuery}/>

        <GraphDisplay showQuery={showQuery}/>
      </div>
    )

}

export default MainContent;