import {
  ChangeDetectionStrategy,
  Component,
  Inject,
  OnInit,
} from '@angular/core';
import { FileUploaderFacadeService } from './facade/file-uploader-facade.service';
import {
  BehaviorSubject,
  EMPTY,
  Subject,
  catchError,
  delay,
  filter,
  of,
  switchMap,
  takeUntil,
  tap,
} from 'rxjs';
import { ApiService } from '../../services/api/api.service';
import { TaskCheckService } from '../../services/task-check/task-check.service';
import { Router } from '@angular/router';
import { NbToastrService } from '@nebular/theme';

@Component({
  selector: 'hackaton-speech2text-glossary-file-uploader-layout',
  templateUrl: './file-uploader-layout.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrls: ['./file-uploader-layout.component.scss'],
})
export class FileUploaderLayoutComponent implements OnInit {
  private readonly audioStatus = new BehaviorSubject<{
    loading: boolean;
    error: boolean;
  }>({
    loading: false,
    error: false,
  });
  private readonly cancelLoad = new Subject<boolean>();
  readonly audioStatus$ = this.audioStatus.asObservable();

  constructor(
    @Inject(FileUploaderFacadeService)
    private readonly facade: FileUploaderFacadeService,
    @Inject(ApiService) private readonly apiService: ApiService,
    @Inject(TaskCheckService)
    private readonly taskCheckService: TaskCheckService,
    @Inject(Router) private readonly router: Router,
    @Inject(NbToastrService) private toastrService: NbToastrService
  ) {}

  ngOnInit() {
    this.facade.uploadedFile
      .pipe(
        filter((file): file is File => !!file),
        tap(() => this.audioStatus.next({ loading: true, error: false })),
        switchMap((file) => this.uploadFile(file)),
        switchMap(({ jobId }) => this.waitUntilTaskComplete(jobId)),
        switchMap((id) =>
          of(this.router.navigate(['/result', id])).pipe(
            delay(3000),
            tap(() => {
              this.audioStatus.next({ loading: false, error: false });
            })
          )
        ),
        catchError(() => {
          this.toastrService.danger(
            'Попробуй ещё раз',
            'Ошибка при распознавании аудио'
          );

          return EMPTY;
        })
      )
      .subscribe();

    this.audioStatus$.pipe(filter(({ error }) => !!error)).subscribe(() => {
      this.cancelLoad.next(true);
      this.cancelLoad.complete();
    });
  }

  cancelLoading() {
    this.cancelLoad.next(true);

    this.cancelLoad.complete();

    this.audioStatus.next({ loading: false, error: false });
  }

  private uploadFile(file: File) {
    return this.apiService.uploadFile(file).pipe(
      catchError((error) => {
        console.log(error);

        this.audioStatus.next({ loading: false, error: true });

        this.toastrService.danger(
          'Попробуй ещё раз',
          'Ошибка при загрузке аудио'
        );

        return EMPTY;
      })
    );
  }

  private waitUntilTaskComplete(jobId: string) {
    return this.taskCheckService
      .checkTaskStatus(jobId)
      .pipe(takeUntil(this.cancelLoad));
  }
}
