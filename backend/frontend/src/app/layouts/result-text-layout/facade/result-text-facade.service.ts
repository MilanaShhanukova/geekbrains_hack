import { Injectable } from '@angular/core';
import { GetResultTextDto } from '@hackaton-speech2text-glossary/dto';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ResultTextFacadeService {
  readonly text = new BehaviorSubject<GetResultTextDto | null>(null);

  // constructor() {}
}
