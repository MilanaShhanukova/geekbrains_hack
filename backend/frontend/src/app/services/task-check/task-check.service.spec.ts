import { TestBed } from '@angular/core/testing';

import { TaskCheckService } from './task-check.service';

describe('TaskCheckService', () => {
  let service: TaskCheckService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TaskCheckService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
