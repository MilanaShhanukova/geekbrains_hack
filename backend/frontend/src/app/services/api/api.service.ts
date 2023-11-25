import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {
  GetResultTextDto,
  JobIdDto,
  TaskStatusDto,
} from '@hackaton-speech2text-glossary/dto';
import { filter, from, of, switchMap } from 'rxjs';

const API_URL = '/v1';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(@Inject(HttpClient) private readonly http: HttpClient) {}

  uploadFile(file: File) {
    const fr = new FileReader();

    fr.readAsDataURL(file);

    // return from(new Promise((resolve) => (fr.onload = resolve))).pipe(
    //   filter((e): e is { target: { result: Blob } } => !!e),
    //   switchMap((e) => {
    //     const file = e.target?.result;

    //     const formData = new FormData();

    //     formData.append('audio', file);

    //     return this.http.post<JobIdDto>(`${API_URL}/upload-file`, formData);
    //   })
    // );

    return of({ jobId: 'test' });
  }

  getTaskStatus(jobId: string) {
    return this.http.get<TaskStatusDto>(`${API_URL}/job/status`, {
      params: {
        job_id: jobId,
      },
    });
  }

  getResutlText(id: string) {
    return this.http.get<GetResultTextDto>(`${API_URL}/job/result`, {
      params: {
        job_id: id,
      },
    });
  }
}
