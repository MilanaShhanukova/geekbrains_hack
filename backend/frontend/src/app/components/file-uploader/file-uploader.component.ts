import {
  ChangeDetectionStrategy,
  Component,
  Inject,
  OnDestroy,
  OnInit,
} from '@angular/core';
import {
  FileUploadControl,
  FileUploadValidators,
} from '@iplab/ngx-file-upload';
import { Subscription } from 'rxjs';
import { FileUploaderFacadeService } from '../../layouts/file-uploader-layout/facade/file-uploader-facade.service';

@Component({
  selector: 'hackaton-speech2text-glossary-file-uploader',
  templateUrl: './file-uploader.component.html',
  styleUrls: ['./file-uploader.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FileUploaderComponent implements OnInit, OnDestroy {
  private subscription!: Subscription;

  public readonly control = new FileUploadControl(
    {
      listVisible: true,
      accept: ['audio/*'],
      discardInvalid: true,
      multiple: false,
    },
    [
      FileUploadValidators.accept(['audio/*']),
      FileUploadValidators.filesLimit(1),
    ]
  );

  constructor(
    @Inject(FileUploaderFacadeService)
    private readonly facade: FileUploaderFacadeService
  ) {}

  ngOnInit() {
    this.subscription = this.control.valueChanges.subscribe(
      (values: Array<File>) => this.getAudio(values[0])
    );
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  private getAudio(file: File): void {
    if (FileReader && file) {
      this.facade.uploadedFile.next(file);
    } else {
      this.facade.uploadedFile.next(null);
    }
  }
}
