import { TestBed } from '@angular/core/testing';

import { ResultTextFacadeService } from './result-text-facade.service';

describe('ResultTextFacadeService', () => {
  let service: ResultTextFacadeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ResultTextFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
