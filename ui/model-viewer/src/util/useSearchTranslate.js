// useSearchTranslate.js

import { useState } from 'react';

export default function useSearchTranslate() {

  const [searchQuery, setSearchQuery] = useState('');
  const [translatedQuery, setTranslatedQuery] = useState('');
  const [showQuery, setShowQuery] = useState(false);

  const translate = (query) => {
    // translation logic
    const translated = query.split('').map(char => char.charCodeAt(0)).join(' ');
    setTranslatedQuery(translated);
  }

  return {
    searchQuery,
    showQuery,
    translatedQuery,
    translate,
    setSearchQuery,
    setTranslatedQuery,
    setShowQuery
  }

}
