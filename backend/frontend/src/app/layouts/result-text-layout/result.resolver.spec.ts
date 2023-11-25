import { TestBed } from '@angular/core/testing';

import { ResultResolver } from './result.resolver';

describe('ResultResolver', () => {
  let resolver: ResultResolver;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    resolver = TestBed.inject(ResultResolver);
  });

  it('should be created', () => {
    expect(resolver).toBeTruthy();
  });
});
