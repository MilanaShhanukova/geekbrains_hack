import { Inject, Injectable } from '@angular/core';
import { ApiService } from '../api/api.service';
import { filter, switchMap, take, timer, map } from 'rxjs';
import { TaskStatusComplete } from '@hackaton-speech2text-glossary/dto';

@Injectable({
  providedIn: 'root',
})
export class TaskCheckService {
  constructor(@Inject(ApiService) private readonly apiService: ApiService) {}

  checkTaskStatus(jobId: string) {
    return timer(0, 5000).pipe(
      switchMap(() => this.apiService.getTaskStatus(jobId)),
      filter(
        (status): status is TaskStatusComplete => status.complete === true
      ),
      take(1),
      map((status) => status.id)
    );
  }
}
