import { TestBed } from '@angular/core/testing';

import { FileUploaderFacadeService } from './file-uploader-facade.service';

describe('FileUploaderFacadeService', () => {
  let service: FileUploaderFacadeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FileUploaderFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
