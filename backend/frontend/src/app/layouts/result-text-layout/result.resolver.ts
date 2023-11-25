import { Inject, Injectable } from '@angular/core';
import {
  Router,
  Resolve,
  RouterStateSnapshot,
  ActivatedRouteSnapshot,
} from '@angular/router';
import { GetResultTextDto } from '@hackaton-speech2text-glossary/dto';

import { ApiService } from '../../services/api/api.service';
import { ResultTextFacadeService } from './facade/result-text-facade.service';
import { tap } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ResultResolver implements Resolve<GetResultTextDto> {
  constructor(
    @Inject(ApiService) private readonly apiService: ApiService,
    @Inject(ResultTextFacadeService)
    private readonly facade: ResultTextFacadeService
  ) {}

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    const id = route.paramMap.get('id');

    if (!id) {
      throw new Error('No id in params');
    }

    return this.apiService
      .getResutlText(id)
      .pipe(tap((result) => this.facade.text.next(result)));
  }
}
