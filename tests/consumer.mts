import { createElement, createRef, type ComponentRef } from 'react';
import { SearchIcon } from '@hugocxl/cxl-icons-react';
import { TerminalIcon } from '@hugocxl/cxl-icons-react/terminal';

createElement(SearchIcon, { size: 24, ref: createRef<SVGSVGElement>(), 'aria-label': 'Search' });
createElement(TerminalIcon, { color: 'red', onClick: event => event.currentTarget.focus() });
// @ts-expect-error size must be numeric
createElement(SearchIcon, { size: 'large' });
