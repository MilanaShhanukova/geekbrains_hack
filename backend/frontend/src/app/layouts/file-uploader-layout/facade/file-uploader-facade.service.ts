import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class FileUploaderFacadeService {
  readonly uploadedFile = new BehaviorSubject<File | null>(null);
}
