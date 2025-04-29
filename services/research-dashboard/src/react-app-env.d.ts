/// <reference types="react-scripts" />

// This file contains type declarations for the environment
// It helps TypeScript recognize JSX elements and other React-specific types

// React and React DOM
declare module 'react' {
  import * as React from 'react';
  
  // React Hooks
  export const useState: typeof React.useState;
  export const useEffect: typeof React.useEffect;
  export const useContext: typeof React.useContext;
  export const useReducer: typeof React.useReducer;
  export const useCallback: typeof React.useCallback;
  export const useMemo: typeof React.useMemo;
  export const useRef: typeof React.useRef;
  export const useImperativeHandle: typeof React.useImperativeHandle;
  export const useLayoutEffect: typeof React.useLayoutEffect;
  export const useDebugValue: typeof React.useDebugValue;
  
  // React Types
  export type FC<P = {}> = React.FC<P>;
  export type ReactNode = React.ReactNode;
  export type ReactElement = React.ReactElement;
  export type CSSProperties = React.CSSProperties;
  export type SyntheticEvent = React.SyntheticEvent;
  export type FormEvent = React.FormEvent;
  export type ChangeEvent = React.ChangeEvent;
  export type MouseEvent = React.MouseEvent;
  export type KeyboardEvent = React.KeyboardEvent;
  
  export = React;
  export as namespace React;
}

declare module 'react-dom' {
  import * as ReactDOM from 'react-dom';
  export = ReactDOM;
  export as namespace ReactDOM;
}

declare module 'react-dom/client' {
  import * as ReactDOMClient from 'react-dom/client';
  export = ReactDOMClient;
  export as namespace ReactDOMClient;
}

// React Router
declare module 'react-router-dom' {
  export interface RouteProps {
    path?: string;
    exact?: boolean;
    component?: React.ComponentType<any>;
    render?: (props: any) => React.ReactNode;
    children?: React.ReactNode | ((props: any) => React.ReactNode);
  }
  
  export const BrowserRouter: React.ComponentType<any>;
  export const Routes: React.ComponentType<any>;
  export const Route: React.ComponentType<RouteProps>;
  export const Link: React.ComponentType<any>;
  export const NavLink: React.ComponentType<any>;
  export const Navigate: React.ComponentType<any>;
  export const Outlet: React.ComponentType<any>;
  export const useNavigate: () => (path: string) => void;
  export const useLocation: () => any;
  export const useParams: () => any;
}

// Material UI
declare module '@mui/material' {
  export const Box: React.ComponentType<any>;
  export const Typography: React.ComponentType<any>;
  export const Paper: React.ComponentType<any>;
  export const Grid: React.ComponentType<any>;
  export const Card: React.ComponentType<any>;
  export const CardContent: React.ComponentType<any>;
  export const CardHeader: React.ComponentType<any>;
  export const CardActions: React.ComponentType<any>;
  export const Divider: React.ComponentType<any>;
  export const LinearProgress: React.ComponentType<any>;
  export const Button: React.ComponentType<any>;
  export const Table: React.ComponentType<any>;
  export const TableBody: React.ComponentType<any>;
  export const TableCell: React.ComponentType<any>;
  export const TableContainer: React.ComponentType<any>;
  export const TableHead: React.ComponentType<any>;
  export const TableRow: React.ComponentType<any>;
  export const Tabs: React.ComponentType<any>;
  export const Tab: React.ComponentType<any>;
  export const AppBar: React.ComponentType<any>;
  export const Toolbar: React.ComponentType<any>;
  export const IconButton: React.ComponentType<any>;
  export const List: React.ComponentType<any>;
  export const ListItem: React.ComponentType<any>;
  export const ListItemButton: React.ComponentType<any>;
  export const ListItemIcon: React.ComponentType<any>;
  export const ListItemText: React.ComponentType<any>;
  export const Drawer: React.ComponentType<any>;
  export const Chip: React.ComponentType<any>;
  export const Stack: React.ComponentType<any>;
  export const Tooltip: React.ComponentType<any>;
  export const Dialog: React.ComponentType<any>;
  export const DialogTitle: React.ComponentType<any>;
  export const DialogContent: React.ComponentType<any>;
  export const DialogContentText: React.ComponentType<any>;
  export const DialogActions: React.ComponentType<any>;
  export const useMediaQuery: (query: any) => boolean;
  export const useTheme: () => any;
}

declare module '@mui/material/styles' {
  export const createTheme: (options: any) => any;
  export const ThemeProvider: React.ComponentType<any>;
}

declare module '@mui/material/CssBaseline' {
  const CssBaseline: React.ComponentType<any>;
  export default CssBaseline;
}

declare module '@mui/icons-material' {
  export const Refresh: React.ComponentType<any>;
  export const Menu: React.ComponentType<any>;
  export const Dashboard: React.ComponentType<any>;
  export const Storage: React.ComponentType<any>;
  export const CloudDownload: React.ComponentType<any>;
  export const Transform: React.ComponentType<any>;
  export const Psychology: React.ComponentType<any>;
  export const MonitorHeart: React.ComponentType<any>;
  export const Settings: React.ComponentType<any>;
  export const CheckCircle: React.ComponentType<any>;
  export const Error: React.ComponentType<any>;
  export const Warning: React.ComponentType<any>;
  export const PlayArrow: React.ComponentType<any>;
  export const Stop: React.ComponentType<any>;
  export const Replay: React.ComponentType<any>;
  export const Info: React.ComponentType<any>;
}

// React Query
declare module '@tanstack/react-query' {
  export const useQuery: (options: any) => any;
  export const QueryClient: any;
  export const QueryClientProvider: React.ComponentType<any>;
}

// Chart.js and React-Chartjs-2
declare module 'chart.js' {
  export const Chart: any;
  export const CategoryScale: any;
  export const LinearScale: any;
  export const PointElement: any;
  export const LineElement: any;
  export const BarElement: any;
  export const Title: any;
  export const Tooltip: any;
  export const Legend: any;
}

declare module 'react-chartjs-2' {
  export const Line: React.ComponentType<any>;
  export const Bar: React.ComponentType<any>;
}

// React Toastify
declare module 'react-toastify' {
  export const ToastContainer: React.ComponentType<any>;
  export const toast: any;
}

// Axios
declare module 'axios' {
  const axios: any;
  export default axios;
  export const create: (config: any) => any;
  
  export interface AxiosRequestConfig {
    baseURL?: string;
    url?: string;
    method?: string;
    headers?: Record<string, string>;
    params?: any;
    data?: any;
    timeout?: number;
    withCredentials?: boolean;
    responseType?: string;
    [key: string]: any;
  }
  
  export interface AxiosResponse<T = any> {
    data: T;
    status: number;
    statusText: string;
    headers: Record<string, string>;
    config: AxiosRequestConfig;
    request?: any;
  }
  
  export interface AxiosError<T = any> extends Error {
    config: AxiosRequestConfig;
    code?: string;
    request?: any;
    response?: AxiosResponse<T>;
    isAxiosError: boolean;
  }
}

// Add JSX runtime declaration for React 17+ new JSX transform
declare module 'react/jsx-runtime' {
  import * as React from 'react';
  export default React;
  export const jsx: typeof React.createElement;
  export const jsxs: typeof React.createElement;
  export const Fragment: typeof React.Fragment;
}

// Node process
declare const process: {
  env: {
    [key: string]: string | undefined;
    NODE_ENV: 'development' | 'production' | 'test';
    REACT_APP_API_URL?: string;
  };
};

declare global {
  namespace JSX {
    interface IntrinsicElements {
      div: React.DetailedHTMLProps<React.HTMLAttributes<HTMLDivElement>, HTMLDivElement>;
      span: React.DetailedHTMLProps<React.HTMLAttributes<HTMLSpanElement>, HTMLSpanElement>;
      strong: React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
      a: React.DetailedHTMLProps<React.AnchorHTMLAttributes<HTMLAnchorElement>, HTMLAnchorElement>;
      p: React.DetailedHTMLProps<React.HTMLAttributes<HTMLParagraphElement>, HTMLParagraphElement>;
      h1: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
      h2: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
      h3: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
      h4: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
      h5: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
      h6: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
      ul: React.DetailedHTMLProps<React.HTMLAttributes<HTMLUListElement>, HTMLUListElement>;
      li: React.DetailedHTMLProps<React.LiHTMLAttributes<HTMLLIElement>, HTMLLIElement>;
      table: React.DetailedHTMLProps<React.TableHTMLAttributes<HTMLTableElement>, HTMLTableElement>;
      tr: React.DetailedHTMLProps<React.HTMLAttributes<HTMLTableRowElement>, HTMLTableRowElement>;
      td: React.DetailedHTMLProps<React.TdHTMLAttributes<HTMLTableDataCellElement>, HTMLTableDataCellElement>;
      th: React.DetailedHTMLProps<React.ThHTMLAttributes<HTMLTableHeaderCellElement>, HTMLTableHeaderCellElement>;
      thead: React.DetailedHTMLProps<React.HTMLAttributes<HTMLTableSectionElement>, HTMLTableSectionElement>;
      tbody: React.DetailedHTMLProps<React.HTMLAttributes<HTMLTableSectionElement>, HTMLTableSectionElement>;
      button: React.DetailedHTMLProps<React.ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>;
      input: React.DetailedHTMLProps<React.InputHTMLAttributes<HTMLInputElement>, HTMLInputElement>;
      form: React.DetailedHTMLProps<React.FormHTMLAttributes<HTMLFormElement>, HTMLFormElement>;
      label: React.DetailedHTMLProps<React.LabelHTMLAttributes<HTMLLabelElement>, HTMLLabelElement>;
      select: React.DetailedHTMLProps<React.SelectHTMLAttributes<HTMLSelectElement>, HTMLSelectElement>;
      option: React.DetailedHTMLProps<React.OptionHTMLAttributes<HTMLOptionElement>, HTMLOptionElement>;
      img: React.DetailedHTMLProps<React.ImgHTMLAttributes<HTMLImageElement>, HTMLImageElement>;
    }
  }
}
