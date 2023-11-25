import { Route } from '@angular/router';
import { ResultResolver } from './layouts/result-text-layout/result.resolver';

export const appRoutes: Route[] = [
  {
    path: 'result/:id',
    resolve: {
      data: ResultResolver,
    },
    loadChildren: () =>
      import('./layouts/result-text-layout/result-text-layout.module').then(
        (m) => m.ResultTextLayoutModule
      ),
  },
  {
    path: '',
    loadChildren: () =>
      import('./layouts/file-uploader-layout/file-uploader-layout.module').then(
        (m) => m.FileUploaderLayoutModule
      ),
  },
];
